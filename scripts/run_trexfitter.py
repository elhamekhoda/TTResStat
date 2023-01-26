import argparse
import datetime
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict
import json

from make_config import (Settings, make_1l_config, make_2l_config,
                         make_combined_config)


def copy_limits_to_shared(channel, mass_out_dir, shared_limit_dir):
    """Copy the limit file to the shared limit directory.
    Args:
        channel (str): '1l', '2l', 'all', or 'combined'
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


def write_configs(settings: Settings):
    """Write the trexfitter config files for the specified channel.
    Returns:
        channel_to_config (Dict[str, Path]): mapping from channel to the path of the config file
        channel_to_opts (Dict[str, str]): mapping from channel to trexfitter options
    """
    ttres1L_config = (settings.mass_out_dir / 'ttres1L.config').resolve()
    ttres2L_config = (settings.mass_out_dir / 'ttres2L.config').resolve()
    ttres1L2L_config = (settings.mass_out_dir / 'ttres1L2L.config').resolve()

    channel_to_config = {}
    channel_to_opts = {}

    if settings.channel == 'all' or settings.channel == '1l':
        template_text, opts = make_1l_config(settings)
        with ttres1L_config.open('w+') as f:
            f.write(template_text)
        channel_to_config['1l'] = ttres1L_config
        channel_to_opts['1l'] = opts
    if settings.channel == 'all' or settings.channel == '2l':
        template_text, opts = make_2l_config(settings)
        with ttres2L_config.open('w+') as f:
            f.write(template_text)
        channel_to_config['2l'] = ttres2L_config
        channel_to_opts['2l'] = opts
    if settings.channel == 'all' or settings.channel == 'combined':
        assert ttres1L_config.exists()
        assert ttres2L_config.exists()
        template_text, opts = make_combined_config(settings, ttres1L_config, ttres2L_config)
        with ttres1L2L_config.open('w+') as f:
            f.write(template_text)
        channel_to_config['combined'] = ttres1L2L_config
        channel_to_opts['combined'] = opts

    return channel_to_config, channel_to_opts

def submit_condor(settings: Settings, args):
    """Submit the trexfitter job to condor."""
    scripts_path = Path(__file__).parent.resolve()
    if args.batch_system == 'af':
        template_name = 'af.tmp'
    elif args.batch_system == 'af_short':
        template_name = 'af_short.tmp'
    elif args.batch_system == 'lxplus_short':
        template_name = 'lxplus_short.tmp'
    template_file = scripts_path / template_name
    with template_file.open('r') as f:
        text = f.read()
    ignore_keys = ['batch_system', 'masses', 'dry_run']
    cmd = [f'--{k} {v}' for k, v in vars(args).items() if v is not None and type(v) is not bool and k not in ignore_keys]
    cmd.extend([f'--{k}' for k, v in vars(args).items() if v is True and k not in ignore_keys])
    cmd.append(f'--mass {settings.mass}')
    cmd = ' '.join(cmd)
    text = text.replace('MASS_DIR', str(settings.mass_out_dir)).replace('SCRIPT_DIR', str(scripts_path)).replace('CMD', cmd)
    condor_sub_file = settings.mass_out_dir / f'condor.sub'
    with condor_sub_file.open('w') as f:
        f.write(text)
    print(f'submitting {str(condor_sub_file)}')
    if not settings.dry_run:
        subprocess.call(['condor_submit', str(condor_sub_file)])

def submit_batch(settings: Settings, args):
    """Submit the trexfitter job to the batch system."""
    if args.batch_system in ['af', 'af_short', 'lxplus_short']:
        submit_condor(settings, args)
    else:
        raise NotImplementedError('Unrecognized batch system: {}'.format(args.batch_system))

def run_trexfitter(settings: Settings, channel_to_config: Dict[str, Path], channel_to_opts: Dict[str, str]):
    """Run trexfitter for the specified parameters.
    Args:
        settings (Settings): settings object
        channel_to_config (Dict[str, Path]): mapping from channel to config file
        channel_to_opts (Dict[str, str]): mapping from channel to trexfitter options
    """
    # make command-line options for trexfitter
    opts = []
    opts.append(f'Signal={settings.signal_name}_{settings.mass}')
    if settings.exclude_systematics:
        opts.append(f'Exclude={",".join(settings.exclude_systematics)}')
    opts = ':'.join(opts)

    def call_trex_fitter(ops: str, opts: str, config: Path, log: str):
        """Call trexfitter with the specified options and config file.
        Args:
            ops (str): trexfitter options
            config (Path): path to the config file
            log (str): name of the log file"""
        cmd = f"""trex-fitter {ops} {str(config)} "{opts}" 2>&1 | tee {log}"""
        run_file = settings.mass_out_dir / 'run.sh'
        with run_file.open('w') as f:
            f.write(cmd)
        subprocess.call(['chmod', '+x', str(run_file)])
        print(f'calling: "{cmd}"')
        if not settings.dry_run:
            os.chdir(settings.mass_out_dir)
            subprocess.call(cmd, shell=True)

    if settings.channel == 'all':
        call_trex_fitter(ops="wfl", opts=channel_to_opts['1l'], config=channel_to_config['1l'], log="ttres1L.ans") #1L
        call_trex_fitter(ops="wfl", opts=channel_to_opts['2l'], config=channel_to_config['2l'], log="ttres2L.ans") #2L
        call_trex_fitter(ops=settings.ops, opts=channel_to_opts['combined'], config=channel_to_config['combined'], log="ttres1L2L.ans") # 1L2L
    elif settings.channel in ['1l', '2l', 'combined']:
        call_trex_fitter(ops=settings.ops, opts=channel_to_opts[settings.channel], config=channel_to_config[settings.channel], log=f"ttres{settings.channel}.ans")
    else:
        raise ValueError(f'Unrecognized channel: {settings.channel}')
    
    if not settings.dry_run and 'l' in settings.ops:
        copy_limits_to_shared(settings.channel, settings.mass_out_dir, settings.limit_dir)

def main():
    parser = argparse.ArgumentParser(description="run single lepton and di-lepton channel combined fit using trex_fitter.")
    parser.add_argument('--seed', default=42, type=int, help="random seed for trex-fitter.")
    parser.add_argument('--dry_run', '-d', action='store_true', help="print trex-fitter commands without running them.")
    parser.add_argument('--suffix', '-s', help="suffix to add to the output directory name.")
    parser.add_argument('--ops', default='mwfl', help="ops for trex-fitter.")
    parser.add_argument('--opts', help="command-line options for trex-fitter (that are not already set in make_config).")
    parser.add_argument('--channel', '-c', default='all', choices=['1l', '2l', 'combined', 'all'], help="perform specified channel only.")
    parser.add_argument('--signal', choices=['zprime', 'grav', 'gluon', 'all'], default='zprime', type=str, help="signal to use.")
    parser.add_argument("--region_1l",       type=str,  default="combined", choices=['boosted', 'resolved', 'combined'],
                            help="Region to use for the 1l channel: boosted, resolved, combined")
    parser.add_argument("--region_2l",       type=str,  default="mllbb_deltaphi", choices=['mllbb', 'deltaphi', 'mllbb_deltaphi'],
                            help="Region to use for the 2l channel: mllbb")
    parser.add_argument("--signal_injection_mass", '-sigm', type=int, default=None, help="mass of signal to inject.")
    parser.add_argument("--signal_injection_name", '-sign', type=str, default=None, choices=['gluon', 'grav', 'zprime'], help="name of signal to inject.")
    parser.add_argument("--unblind", action='store_true', help='unblind the analysis, if set')
    parser.add_argument("--auto_injection_strength", type=float, help='injection strength for TRExFitter auto signal injection, if set')
    parser.add_argument("--use_dilep_names", action="store_true", help="use dilepton naming scheme for systematics.")
    parser.add_argument("--statonly", action="store_true", help="run stat-only fit.")
    parser.add_argument("--bonly", action="store_true", help="run b-only fit.")
    parser.add_argument('--fit_mu_asimov', type=float, default=1.0, help="mu value for fit asimov data.")
    parser.add_argument('--batch_system', choices=['af', 'af_short', 'lxplus_short'], default=None, type=str, help="submit jobs to specified batch system.")
    parser.add_argument('--masses', '-m', default=None, type=str, help="Signal masses to scan (comma-separated list, e.g., 400,500,750).")

    args = parser.parse_args()

    if args.channel not in ['combined', 'all']:
        if 'm' in args.ops:
            raise ValueError('Cannot run single channel fits with the "m" option.')

    # Make appropriate directories
    timestamp = str(datetime.date.today())
    run_name = f'statResults_ttres1L2L_{timestamp}'
    if not args.suffix:
        suffix = [f'{args.channel}', f'{args.signal}']
        if args.channel in ['1l', 'all']:
            suffix.append(f'region1l-{args.region_1l}')
        if args.channel in ['2l', 'all']:
            suffix.append(f'region2l-{args.region_2l}')
        if args.unblind:
            suffix.append('unblind')
        if args.statonly:
            suffix.append('statonly')
        if args.bonly:
            suffix.append('bonly')
        if args.signal_injection_mass:
            suffix.append(f'siginject-{args.signal_injection_name}-{args.signal_injection_mass}')
        if args.auto_injection_strength:
            suffix.append(f'autoinject-{args.auto_injection_strength}')
        if args.opts:
            raise NotImplementedError('Cannot use opts with default suffix. Please specify a suffix.')
        
        suffix = '_'.join(suffix)
    else:
        suffix = args.suffix
    run_name = run_name + '_' + suffix
    scripts_path = Path(__file__).parent.resolve()
    run_dir = (scripts_path / '..' / 'run' / run_name).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    limit_dir = (run_dir / 'limits').resolve()
    limit_dir.mkdir(exist_ok=True)
    histo_dir = (scripts_path / '..' / 'histograms').resolve()

    print(f'run_dir: {run_dir}')
    print(f'limit_dir: {limit_dir}')

    settings_json = run_dir / 'settings.json'

    with open(settings_json, 'w') as f:
        json.dump(vars(args), f, indent=4)

    exclude_systematics = []
    # set the signal name
    if args.signal == 'zprime':
        signal_name = 'ZprimeTC2'
    elif args.signal == 'grav':
        signal_name = 'Grav'
    elif args.signal == 'gluon':
        signal_name = 'KKg'
    elif args.signal == 'all':
        signal_name = 'all'
    else:
        raise NotImplementedError(f'Unknown signal {args.signal}')


    # Set mass points to scan
    if args.masses is None:
        if args.signal == 'zprime':
            masses = [500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000, 5000]
        elif args.signal == 'grav':
            masses = [400, 500, 750, 1000, 2000, 3000]
        elif args.signal == 'gluon':
            masses = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    else:
        masses = args.masses.split(',')

    # Run trexfitter for each mass point
    for mass in masses:
        mass = int(mass)
        mass_out_dir = (run_dir / f'{args.signal}_{str(mass)}').resolve()
        mass_out_dir.mkdir(exist_ok=True, parents=True)
        
        settings = Settings(mass_out_dir=mass_out_dir, channel=args.channel, mass=mass, signal_name=signal_name, region_1l=args.region_1l, region_2l=args.region_2l, use_dilep_names=args.use_dilep_names, 
                            signal_injection_mass=args.signal_injection_mass, signal_injection_name=args.signal_injection_name, 
                            unblind=args.unblind, auto_injection_strength=args.auto_injection_strength, statonly=args.statonly, 
                            bonly=args.bonly, ops=args.ops, limit_dir=limit_dir, exclude_systematics=exclude_systematics, dry_run=args.dry_run, histo_dir=histo_dir, fit_mu_asimov=args.fit_mu_asimov)

        channel_to_config, channel_to_opts = write_configs(settings)

        if args.batch_system:
            submit_batch(settings, args)
        else:
            run_trexfitter(settings=settings, channel_to_config=channel_to_config, channel_to_opts=channel_to_opts)

if __name__ == "__main__":
    main()