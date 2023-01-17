import shutil
import subprocess
import argparse
from pathlib import Path
import datetime
import os

def copy_limits_to_shared(channel, mass, mass_out_dir, shared_limit_dir):
    """Copy the limit file to the shared limit directory.
    Args:
        channel (str): '1l', '2l', 'all', or 'combined'
        mass (int): Z' mass
        mass_out_dir (Path): directory containing the limit file from running trexfitter
        shared_limit_dir (Path): directory to copy the limit file to
    """
    if channel == 'all' or channel == 'combined':
        limit_run = 'ttRes1L2L'
    elif channel == '2l':
        limit_run = 'ttRes2L'
    elif channel == '1l':
        limit_run = 'ttRes1L'
    run_limit_dir = mass_out_dir / limit_run / 'Limits' / 'asymptotics'
    try:
        limit_file = [f for f in run_limit_dir.glob('*.root')][0]
        shared_file = shared_limit_dir / limit_file.name
        print('copying limit file from run limit directory: ', limit_file, ' to shared limit directory: ', shared_file)
        shutil.copy(limit_file, shared_file)
    except IndexError:
        print('error: no limit file found in run limit directory: ', run_limit_dir)


def write_configs(mass_out_dir, config_dir, channel, mass, signal_name):
    """Write the trexfitter config files for the specified channel.
    Args:
        mass_out_dir (Path): directory to write the config files to
        config_dir (Path): directory containing the config file templates
        channel (str): '1l', '2l', 'all', or 'combined'
        mass (int): Z' mass
        signal_name (str): name of the signal sample
    Returns:
        ttres1L_config (Path): path to the ttres1L.config file
        ttres2L_config (Path): path to the ttres2L.config file
        ttres1L2L_config (Path): path to the ttres1L2L.config file
    """
    ttres1L_config_template = (config_dir / 'ttres1L.config').resolve()
    ttres2L_config_template = (config_dir / 'ttres2L.config').resolve()
    ttres1L2L_config_template = (config_dir / 'ttres1L2L.config').resolve()

    ttres1L_config = (mass_out_dir / 'ttres1L.config').resolve()
    ttres2L_config = (mass_out_dir / 'ttres2L.config').resolve()
    ttres1L2L_config = (mass_out_dir / 'ttres1L2L.config').resolve()

    if channel == 'all' or channel == '1l':
        with ttres1L_config_template.open('r') as f:
            template_text = f.read()
            template_text = template_text.replace("OUTPUTDIR", str(mass_out_dir)).replace("ZPRIMEMASS", str(mass)).replace("SIGNALNAME", signal_name).replace("SIGNALMASS", str(mass))
        with ttres1L_config.open('w+') as f:
            f.write(template_text)
    if channel == 'all' or channel == '2l':
        with ttres2L_config_template.open('r') as f:
            template_text = f.read()
            template_text = template_text.replace("OUTPUTDIR", str(mass_out_dir))
        with ttres2L_config.open('w+') as f:
            f.write(template_text)
    if channel == 'all' or channel == 'combined':
        assert ttres1L_config.exists()
        assert ttres2L_config.exists()
        with ttres1L2L_config_template.open('r') as f:
            template_text = f.read()
            template_text = template_text.replace("SIGNALNAME", signal_name).replace("SIGNALMASS", str(mass)).replace("SINGLELEPCONFIG", str(ttres1L_config)).replace("DILEPCONFIG", str(ttres2L_config))
        with ttres1L2L_config.open('w+') as f:
            f.write(template_text)
    return ttres1L_config, ttres2L_config, ttres1L2L_config

def submit_condor(mass_out_dir, mass, channel, ops, suffix, dry_run, batch_system, signal, exclude_systematics):
    """Submit the trexfitter job to condor.
    Args:
        mass_out_dir (Path): directory to run trexfitter in
        mass (int): Z' mass
        channel (str): '1l', '2l', 'all', or 'combined'
        ops (str): options to pass to trexfitter
        suffix (str): suffix to append to the output directory
        dry_run (bool): if True, don't submit the job
        batch_system (str): 'af' or 'af_short'
        signal (str): name of the signal sample
        exclude_systematics (bool): if True, don't run the problematic systematics"""
    scripts_path = Path(__file__).parent.resolve()
    if batch_system == 'af':
        template_name = 'af.tmp'
    elif batch_system == 'af_short':
        template_name = 'af_short.tmp'
    template_file = scripts_path / template_name
    with template_file.open('r') as f:
        text = f.read()
    text = text.replace('MASS_DIR', str(mass_out_dir)).replace('SCRIPTS', str(scripts_path)).replace('CHANNEL', channel)
    text = text.replace('OPS', ops).replace('SUFFIX', suffix).replace('MASS', str(mass)).replace('SIGNAL', signal)
    if exclude_systematics:
        text = text.replace('EXCLUDE_SYSTEMATICS', '--exclude-systematics')
    else:
        text = text.replace('EXCLUDE_SYSTEMATICS', '')
    condor_sub_file = mass_out_dir / f'condor.sub'
    with condor_sub_file.open('w') as f:
        f.write(text)
    print(f'submitting {str(condor_sub_file)}')
    if not dry_run:
        subprocess.call(['condor_submit', str(condor_sub_file)])

def submit_batch(mass_out_dir, mass, channel, ops, suffix, dry_run, batch_system, signal, exclude_systematics):
    """Submit the trexfitter job to the batch system.
    Args:
        mass_out_dir (Path): directory to run trexfitter in
        mass (int): Z' mass
        channel (str): '1l', '2l', 'all', or 'combined'
        ops (str): trexfitter options
        suffix (str): suffix to append to the output directory
        dry_run (bool): if True, don't actually submit the job
        batch_system (str): 'af' or 'af_short'
        signal (str): name of the signal
        exclude_systematics (bool): if True, don't run the problematic systematics
    """
    if batch_system in ['af', 'af_short']:
        submit_condor(mass_out_dir, mass, channel, ops, suffix, dry_run, batch_system, signal, exclude_systematics)
    else:
        raise NotImplementedError('Unrecognized batch system: {}'.format(batch_system))

def run_trexfitter(mass_out_dir, channel, ops, dry_run, ttres1L_config, ttres2L_config, ttres1L2L_config, mass, limit_dir, exclude_systematics, signal_name):
    """Run trexfitter for the specified parameters.
    Args:
        mass_out_dir (Path): directory to run trexfitter in
        channel (str): '1l', '2l', 'all', or 'combined'
        ops (str): trexfitter options
        dry_run (bool): if True, don't actually run trexfitter
        ttres1L_config (Path): path to the ttres1L.config file
        ttres2L_config (Path): path to the ttres2L.config file
        ttres1L2L_config (Path): path to the ttres1L2L.config file
        mass (int): Z' mass
        limit_dir (Path): directory to store the limit files in
        exclude_systematics (List): list of systematics to exclude
        signal_name (str): name of the signal to use
    """
    # make command-line options for trexfitter
    opts = []
    opts.append(f'Signal={signal_name}_{mass}')
    if exclude_systematics:
        opts.append(f'Exclude={",".join(exclude_systematics)}')
    opts = ':'.join(opts)

    def call_trex_fitter(ops, config, log):
        """Call trexfitter with the specified options and config file.
        Args:
            ops (str): trexfitter options
            config (Path): path to the config file
            log (str): name of the log file"""
        cmd = f"""trex-fitter {ops} {str(config)} "{opts}" 2>&1 | tee {log}"""
        run_file = mass_out_dir / 'run.sh'
        with run_file.open('w') as f:
            f.write(cmd)
        subprocess.call(['chmod', '+x', str(run_file)])
        print(f'calling: "{cmd}"')
        if not dry_run:
            os.chdir(mass_out_dir)
            subprocess.call(cmd, shell=True)

    if channel == 'all':
        call_trex_fitter(ops="hwfl", config=ttres1L_config, log="ttres1L.ans") #1L
        call_trex_fitter(ops="wfl", config=ttres2L_config, log="ttres2L.ans") #2L
        call_trex_fitter(ops=ops, config=ttres1L2L_config, log="ttres1L2L.ans") # 1L2L
    elif channel == '1l':
        call_trex_fitter(ops=ops, config=ttres1L_config, log="ttres1L.ans") #1L
    elif channel == '2l':
        call_trex_fitter(ops=ops, config=ttres2L_config, log="ttres2L.ans") #2L
    elif channel == 'combined':
        call_trex_fitter(ops=ops, config=ttres1L2L_config, log="ttres1L2L.ans") # 1L2L
    else:
        raise NotImplementedError()

    if not dry_run and 'l' in ops:
        copy_limits_to_shared(channel, mass, mass_out_dir, limit_dir)
    

def main():
    parser = argparse.ArgumentParser(description="run single lepton and di-lepton channel combined fit using trex_fitter.")
    parser.add_argument('config_dir', help="directory containing ttres1L.config, ttres2L.config and ttres1L2L.config.")
    parser.add_argument('--masses', '-m', default=[500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000, 5000], type=int, nargs='+', help="Z' masses to scan.")
    parser.add_argument('--suffix', '-s', default="", help="suffix to add to the output directory name.")
    parser.add_argument('--ops', default='mwfl', help="ops for trex-fitter.")
    parser.add_argument('--channel', '-c', default='all', choices=['1l', '2l', 'combined', 'all'], help="perform specified channel only.")
    parser.add_argument('--dry_run', '-d', action='store_true', help="print trex-fitter commands without running them.")
    parser.add_argument('--batch_system', choices=['af', 'af_short'], default=None, type=str, help="submit jobs to specified batch system.")
    parser.add_argument('--signal', choices=['zprime', 'grav', 'gluon'], default='zprime', type=str, help="signal to use.")
    parser.add_argument('--exclude_systematics', action='store_true', help="exclude problematic systematics from the fit.")

    args = parser.parse_args()

    if args.channel not in ['combined', 'all']:
        if 'm' in args.ops:
            raise ValueError('Cannot run single channel fits with the "m" option.')

    # Make appropriate directories
    timestamp = str(datetime.date.today())
    run_name = f'statResults_ttres1L2L_{timestamp}'
    if args.suffix:
        run_name = run_name + '_' + args.suffix
    if not args.suffix and args.batch:
        raise NotImplementedError('batch mode must be run with a suffix!')
    scripts_path = Path(__file__).parent.resolve()
    run_dir = (scripts_path / '..' / 'run' / run_name).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    limit_dir = (run_dir / 'limits').resolve()
    limit_dir.mkdir(exist_ok=True)
    config_dir = Path(args.config_dir).resolve()

    print(f'run_dir: {run_dir}')
    print(f'limit_dir: {limit_dir}')
    
    # if exclude_systematics, set the list of systematics to exclude from the config file
    if args.exclude_systematics:
        exclude_systematics = 'ttbar_PS_Shape,ttbar_PS_Acc,ttbar_PS_noRew_Shape,ttbar_PS_noRew_Acc,ttbar_ME_old_Shape,ttbar_ME_old_Acc,ttbar_ISR_hdamp_Shape,ttbar_ISR_hdamp_Acc,ttbar_FSR_Shape,ttbar_FSR_Acc'.split(',')
    else:
        exclude_systematics = []
    # set the signal name
    if args.signal == 'zprime':
        signal_name = 'ZprimeTC2'
    elif args.signal == 'grav':
        signal_name = 'Grav'
    elif args.signal == 'gluon':
        signal_name = 'KKg'
    else:
        raise NotImplementedError(f'Unknown signal {args.signal}')

    # Run trexfitter for each mass point
    for mass in args.masses:
        mass_out_dir = (run_dir / f'{args.signal}_{str(mass)}').resolve()
        mass_out_dir.mkdir(exist_ok=True, parents=True)

        ttres1L_config, ttres2L_config, ttres1L2L_config = write_configs(mass_out_dir, config_dir, args.channel, mass, signal_name)

        if args.batch_system:
            submit_batch(mass_out_dir, mass, args.channel, args.ops, args.suffix, args.dry_run, args.batch_system, args.signal, args.exclude_systematics)
        else:
            run_trexfitter(mass_out_dir, args.channel, args.ops, args.dry_run, ttres1L_config, ttres2L_config, ttres1L2L_config, mass, limit_dir, exclude_systematics, signal_name)


if __name__ == "__main__":
    main()