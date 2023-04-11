import argparse
from pathlib import Path
import ROOT

bad_samples = ['zjets_LF_up', 'zjets_HF_up']

lumi = 139000 % 36100 + 44300 + 58600


def convert_histos_in_file(tfile, out_dir, path=''):
    for key in tfile.GetListOfKeys():
        obj = key.ReadObj()
        if obj.InheritsFrom("TDirectory"):
            # If this is a directory, recurse into it
            if path == '':
                new_path = key.GetName()
            else:
                new_path = path + '/' + key.GetName()
            print(f"\t Recursing into {new_path}...")
            convert_histos_in_file(obj, out_dir, new_path)
        elif obj.InheritsFrom("TH1"):
            name = obj.GetName()
            if name.endswith('_orig') or name.endswith('_regBin'):
                continue
            # If this is a histogram, convert it to the ttres1L format
            path_parts = path.split("/")
            region = path_parts[0]
            sample = path_parts[1]
            systematic = path_parts[2]
            # remove 'region_sample_systematic_' from the name to get the variation
            variation = name[len(region) + len(sample) + len(systematic) + 3:]
            if sample in bad_samples:
                print(f"\t\t Ignoring bad sample {sample}...")
                continue
            if systematic == 'Lumi':
                continue
            # write lowercase
            region = region.lower()
            sample = sample.lower()
            # add _dilep to the sample name
            if 'data' not in sample:
                sample = sample + '_dilep'
            out_file = out_dir / f"{region}/hist_{sample}.root"
            print(f"\t\t {out_file}")
            out_file.parent.mkdir(exist_ok=True, parents=True)
            out_tfile = ROOT.TFile(str(out_file), "UPDATE")
            out_tfile.cd()
            # divide the weights by the luminosity, as it will be added back in later
            # obj.Scale(1./lumi)
            # write the histogram as a clone, so that the original histogram is not modified
            if systematic == 'nominal':
                print(f"\t\t\t {region}")
                obj.Write(region)
            else:
                print(f"\t\t\t {region}_{systematic}_{variation}")
                obj.Write(f"{region}_{systematic}_{variation}")
            out_tfile.Close()
            # cd back to the original directory
            tfile.cd()


def convert_histos(histo_dir, out_dir):
    """Converts histograms from trexfitter format to similar format used by ttres1L. This is needed for the 2L analysis.

    In trexfitter, each region has its own histogram file, e.g., ttRes2L_fit_inverted_deltaEta_2dRew_slim_SysAll_V24_DeltaPhi_histos.root.
    Within each histogram file, there are multiple histograms, corresponding to each sample and systematic. 
    For example, /mllbb_DeltaPhi000to050/ttbar_dilep_hdamp/nominal/mllbb_DeltaPhi000to050_ttbar_dilep_hdamp is the path to the nominal histogram for the ttbar_dilep_hdamp sample in the mllbb_DeltaPhi000to050 region.
    Similarly, /mllbb_DeltaPhi000to050/KKgPY2000/Lumi/mllbb_DeltaPhi000to050_KKgPY2000_Lumi_Up is the path to the up variation of the Lumi systematic for the KKgPY2000 sample in the mllbb_DeltaPhi000to050 region.

    In ttres1L, each region has its own histogram directory. Furthermore, each sample has its own histogram file, e.g., be/hist_qcd.root.
    Within each histogram file, there are multiple histograms, several for each systematic (corresponding to up and/or down variations), and one nominal histogram.

    This function converts the trexfitter histograms to the ttres1L format.
    """

    # iterate over all histogram files in the input directory
    for histo_file in histo_dir.iterdir():
        print(f"Converting {histo_file}...")
        if not histo_file.is_file():
            continue
        if not histo_file.name.endswith('.root'):
            continue
        tfile = ROOT.TFile(str(histo_file))
        convert_histos_in_file(tfile, out_dir)
        # close the input file
        tfile.Close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('histo_dir', type=str,
                        help='Path to the histogram directory')
    parser.add_argument('out_dir', type=str,
                        help='Path to the output directory')

    args = parser.parse_args()

    histo_dir = Path(args.histo_dir)
    out_dir = Path(args.out_dir)

    out_dir.mkdir(exist_ok=True, parents=True)

    convert_histos(histo_dir, out_dir)


if __name__ == "__main__":
    main()
