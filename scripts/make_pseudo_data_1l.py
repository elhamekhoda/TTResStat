from pathlib import Path
import argparse
from shutil import copyfile, rmtree

from ROOT import TFile, TH1F

# def make_pseudodata(root_dir, signal_name):
#     # iterate over all subdirectories in root_dir
#     for channel_dir in root_dir.iterdir():
#         signal_paths = [f for f in channel_dir.glob(f'hist_{signal_name}*.root')]
#         backgrounds = ['tt', 'wjets', 'singletop', 'zjets', 'vv']
#         background_paths = [str(channel_dir / f'hist_{b}.root') for b in backgrounds]
#         for p in signal_paths:
#             subprocess.call(['hadd', str(channel_dir / f'{p.stem}_pseudodata.root'), str(p)] + background_paths)

def get_contents(histogram):
    contents = []
    for bin in range(histogram.GetNbinsX()):
        contents.append(histogram.GetBinContent(bin))
    return contents

def get_errors(histogram):
    errors = []
    for bin in range(histogram.GetNbinsX()):
        errors.append(histogram.GetBinError(bin))
    return errors

def make_pseudo_data(signal_name, mass, mu):
    """Generate pseudo-data for the specified parameters."""
    
    scripts_path = Path(__file__).parent.resolve()
    histo_dir = (scripts_path / '..' / 'histograms').resolve()

    original_trexfitter_histograms = histo_dir / 'ttres1l/tt1lep_config_wbtagSR_1b2b'
    injected_trexfitter_histograms = histo_dir / f'ttres1l/tt1lep_config_wbtagSR_1b2b_signal_injection/{signal_name}_{mass}_mu{mu}'
    if injected_trexfitter_histograms.exists():
        print(f'Pseudo-data already exists for {signal_name} {mass}. Deleting...')
        rmtree(injected_trexfitter_histograms)
    injected_trexfitter_histograms.mkdir(parents=True, exist_ok=True)
    # copy histo files from original to new directory
    for f in original_trexfitter_histograms.glob('*.root'):
        print(f'Copying {f} to {injected_trexfitter_histograms / f.name}')
        copyfile(f, injected_trexfitter_histograms / f.name)

    backgrounds = ['tt', 'wjets', 'singletop', 'qcd', 'zjets', 'diboson']
    
    for region in "be1,be2,be3,re1,re2,re3,bmu1,bmu2,bmu3,rmu1,rmu2,rmu3".split(','):
        print(f'Injecting signal into {region}...')
        histo_path = injected_trexfitter_histograms / f'ttRes1L_{region}_histos.root'
        trex_histogram_tfile = TFile(str(histo_path), 'update')

        
        signal_histogram_name = f'{region}/{signal_name}_{mass}/nominal/{region}_{signal_name}_{mass}'
        print('\t Getting signal histogram: ', signal_histogram_name)
        h_asimov = trex_histogram_tfile.Get(signal_histogram_name)
        h_asimov.Scale(mu)
        # print('\t\t signal contents: ', get_contents(h_asimov))
        # print('\t\t signal errors: ', get_errors(h_asimov))
        for b in backgrounds:
            background_histogram_name = f'{region}/{b}/nominal/{region}_{b}'
            print('\t Getting background histogram: ', background_histogram_name)
            h_background = trex_histogram_tfile.Get(background_histogram_name)
            if b == 'qcd':
                h_background_f = TH1F()
                h_background.Copy(h_background_f)
                h_background = h_background_f
            # print('\t\t background contents: ', get_contents(h_background))
            # print('\t\t background errors: ', get_errors(h_background))
            h_asimov = h_asimov + h_background

        data_histogram_name = f'{region}/Data/nominal/{region}_Data'
        print('\t Writing asimov data histogram: ', data_histogram_name)
        print('\t\t Asimov contents: ', get_contents(h_asimov))
        print('\t\t Asimov errors: ', get_errors(h_asimov))

        h_asimov.SetName(data_histogram_name)
        h_asimov.Write()
        trex_histogram_tfile.Close()

def main():
    parser = argparse.ArgumentParser(description='Make pseudo-data for a given signal.')
    parser.add_argument("--signal_injection_mass", '-sigm', type=int, default=None, help="mass of signal to inject.")
    parser.add_argument("--signal_injection_name", '-sign', type=str, default=None, choices=['gluon', 'grav', 'zprime'], help="name of signal to inject.")
    parser.add_argument("--mu_injection", '-mu', type=float, default=1.0, help="mu value to inject.")

    args = parser.parse_args()
    if args.signal_injection_name == 'zprime':
        signal_name = 'ZprimeTC2'
    elif args.signal_injection_name == 'grav':
        signal_name = 'Grav'
    elif args.signal_injection_name == 'gluon':
        signal_name = 'KKg'
    else:
        raise NotImplementedError(f'Unknown signal {args.signal_injection_name}')

    make_pseudo_data(signal_name, args.signal_injection_mass, args.mu_injection)


if __name__ == '__main__':
    main()