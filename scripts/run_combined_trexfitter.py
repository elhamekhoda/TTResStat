import subprocess
import argparse
from pathlib import Path
import datetime
import os



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_dir')
    parser.add_argument('--masses', '-m', default=[400, 500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000, 5000], type=int, nargs='+')
    parser.add_argument('--suffix', '-s', default="")
    parser.add_argument('--ops', default='mwfl')
    parser.add_argument('--skip_individual', action='store_true')

    args = parser.parse_args()
    masses = args.masses

    config_dir = Path(args.config_dir)
    ttres1L_config_template = (config_dir / 'ttres1L.config').resolve()
    ttres2L_config_template = (config_dir / 'ttres2L.config').resolve()
    ttres1L2L_config_template = (config_dir / 'ttres1L2L.config').resolve()

    timestamp = str(datetime.date.today())
    out_name = f'statResults_ttres1L2L_{timestamp}'
    if args.suffix:
        out_name = out_name + '_' + args.suffix
    out_dir = (Path('run') / out_name).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    limit_dir = (out_dir / 'limits').resolve()
    limit_dir.mkdir(exist_ok=True)

    def call_trex_fitter(ops, config, mass, log):
        cmd = f"""trex-fitter {ops} {config} "Signal=ZprimeTC2_{mass}" 2>&1 | tee {log}"""
        subprocess.call(cmd, shell=True)

    for mass in masses:
        mass_out_dir = (out_dir / f'zprime_{str(mass)}').resolve()
        mass_out_dir.mkdir(exist_ok=True, parents=True)

        ttres1L_config = (mass_out_dir / 'ttres1L.config').resolve()
        ttres2L_config = (mass_out_dir / 'ttres2L.config').resolve()
        ttres1L2L_config = (mass_out_dir / 'ttres1L2L.config').resolve()

        with ttres1L_config_template.open('r') as f:
            template_text = f.read()
            template_text = template_text.replace("OUTPUTDIR", str(mass_out_dir))
        with ttres1L_config.open('w+') as f:
            f.write(template_text)
        with ttres2L_config_template.open('r') as f:
            template_text = f.read()
            template_text = template_text.replace("OUTPUTDIR", str(mass_out_dir))
        with ttres2L_config.open('w+') as f:
            f.write(template_text)
        with ttres1L2L_config_template.open('r') as f:
            template_text = f.read()
            template_text = template_text.replace("ZPRIMEMASS", str(mass)).replace("SINGLELEPCONFIG", str(ttres1L_config)).replace("DILEPCONFIG", str(ttres2L_config))
        with ttres1L2L_config.open('w+') as f:
            f.write(template_text)

        os.chdir(mass_out_dir)
        if not args.skip_individual: # run individual fits first
            call_trex_fitter(ops="hwfl", config=str(ttres1L_config), mass=mass, log="ttres1L.ans") #1L
            call_trex_fitter(ops="wfl", config=str(ttres2L_config), mass=mass, log="ttres2L.ans") #2L
        call_trex_fitter(ops=args.ops, config=str(ttres1L2L_config), mass=mass, log="ttres1L2L.ans") # 1L2L

        limit_file = mass_out_dir / 'ttRes1L2L' / 'Limits' / 'asymptotics' / 'myLimit_BLIND_CL95.root'
        limit_file.rename(limit_dir / f'zprime{mass}.root')






if __name__ == "__main__":
    main()