import subprocess
import argparse
from pathlib import Path
import datetime
import os



def main():
    parser = argparse.ArgumentParser(description="run single lepton and di-lepton channel combined fit using trex_fitter.")
    parser.add_argument('config_dir', help="directory containing ttres1L.config, ttres2L.config and ttres1L2L.config.")
    parser.add_argument('--masses', '-m', default=[400, 500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000, 5000], type=int, nargs='+', help="Z' masses to scan.")
    parser.add_argument('--suffix', '-s', default="", help="suffix to add to the output directory name.")
    parser.add_argument('--ops', default='mwfl', help="ops for trex-fitter.")
    parser.add_argument('--channel', '-c', default='all', choices=['1l', '2l', 'combined', 'all'], help="perform specified channel only.")
    parser.add_argument('--dry_run', '-d', action='store_true', help="print trex-fitter commands without running them.")
    parser.add_argument('--batch', action='store_true', help="submit jobs to condor.")

    args = parser.parse_args()

    config_dir = Path(args.config_dir)
    ttres1L_config_template = (config_dir / 'ttres1L.config').resolve()
    ttres2L_config_template = (config_dir / 'ttres2L.config').resolve()
    ttres1L2L_config_template = (config_dir / 'ttres1L2L.config').resolve()

    timestamp = str(datetime.date.today())
    out_name = f'statResults_ttres1L2L_{timestamp}'
    if args.suffix:
        out_name = out_name + '_' + args.suffix
    if not args.suffix and args.batch:
        raise NotImplementedError('batch mode must be run with a suffix!')
    out_dir = (Path('run') / out_name).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    limit_dir = (out_dir / 'limits').resolve()
    limit_dir.mkdir(exist_ok=True)

    def call_trex_fitter(ops, config, mass, log, mass_out_dir):
        cmd = f"""trex-fitter {ops} {str(config)} "Signal=ZprimeTC2_{mass}" 2>&1 | tee {log}"""
        print(f'calling: "{cmd}"')
        if not args.dry_run:
            os.chdir(mass_out_dir)
            subprocess.call(cmd, shell=True)
            
    
    for mass in args.masses:
        mass_out_dir = (out_dir / f'zprime_{str(mass)}').resolve()
        mass_out_dir.mkdir(exist_ok=True, parents=True)

        ttres1L_config = (mass_out_dir / 'ttres1L.config').resolve()
        ttres2L_config = (mass_out_dir / 'ttres2L.config').resolve()
        ttres1L2L_config = (mass_out_dir / 'ttres1L2L.config').resolve()

        if args.channel == 'all' or args.channel == '1l':
            with ttres1L_config_template.open('r') as f:
                template_text = f.read()
                template_text = template_text.replace("OUTPUTDIR", str(mass_out_dir)).replace("ZPRIMEMASS", str(mass))
            with ttres1L_config.open('w+') as f:
                f.write(template_text)
        if args.channel == 'all' or args.channel == '2l':
            with ttres2L_config_template.open('r') as f:
                template_text = f.read()
                template_text = template_text.replace("OUTPUTDIR", str(mass_out_dir))
            with ttres2L_config.open('w+') as f:
                f.write(template_text)
        if args.channel == 'all' or args.channel == 'combined':
            assert ttres1L_config.exists()
            assert ttres2L_config.exists()
            with ttres1L2L_config_template.open('r') as f:
                template_text = f.read()
                template_text = template_text.replace("ZPRIMEMASS", str(mass)).replace("SINGLELEPCONFIG", str(ttres1L_config)).replace("DILEPCONFIG", str(ttres2L_config))
            with ttres1L2L_config.open('w+') as f:
                f.write(template_text)

        if args.batch:
            scripts_path = Path(__file__).parent.resolve()
            template_file = scripts_path / 'condor.tmp'
            with template_file.open('r') as f:
                text = f.read()
            text = text.replace('MASS_DIR', str(mass_out_dir)).replace('SCRIPTS', str(scripts_path)).replace('CHANNEL', args.channel)
            text = text.replace('OPS', args.ops).replace('SUFFIX', args.suffix).replace('MASS', str(mass))
            condor_sub_file = mass_out_dir / f'condor.sub'
            with condor_sub_file.open('w') as f:
                f.write(text)
            print(f'submitting {str(condor_sub_file)}')
            if not args.dry_run:
                subprocess.call(['condor_submit', str(condor_sub_file)])
        else:
            if args.channel == 'all':
                call_trex_fitter(ops="hwfl", config=ttres1L_config, mass=mass, log="ttres1L.ans", mass_out_dir=mass_out_dir) #1L
                call_trex_fitter(ops="wfl", config=ttres2L_config, mass=mass, log="ttres2L.ans", mass_out_dir=mass_out_dir) #2L
                call_trex_fitter(ops=args.ops, config=ttres1L2L_config, mass=mass, log="ttres1L2L.ans", mass_out_dir=mass_out_dir) # 1L2L
            elif args.channel == '1l':
                call_trex_fitter(ops=args.ops, config=ttres1L_config, mass=mass, log="ttres1L.ans", mass_out_dir=mass_out_dir) #1L
            elif args.channel == '2l':
                call_trex_fitter(ops=args.ops, config=ttres2L_config, mass=mass, log="ttres2L.ans", mass_out_dir=mass_out_dir) #2L
            elif args.channel == 'combined':
                call_trex_fitter(ops=args.ops, config=ttres1L2L_config, mass=mass, log="ttres1L2L.ans", mass_out_dir=mass_out_dir) # 1L2L
            else:
                raise NotImplementedError()
        
        if not args.dry_run and (not args.channel or args.channel == 'combined') and 'l' in args.ops:
            limit_file = mass_out_dir / 'ttRes1L2L' / 'Limits' / 'asymptotics' / 'myLimit_BLIND_CL95.root'
            limit_file.rename(limit_dir / f'zprime{mass}.root')


if __name__ == "__main__":
    main()