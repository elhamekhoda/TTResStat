import ROOT
import argparse
from pathlib import Path


def compare_tfile_weights(file1, file2):
    """For each histogram in the unnormalized tfile, compare the weights to the normalized tfile and check for differences."""
    # Define a function to recursively loop over all histograms in a directory
    equivalent_histograms = []
    different_histograms = []
    def loop_directory(directory, directory_path):
        for key in directory.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, ROOT.TDirectory):
                # Recursively loop over all histograms in the subdirectory
                loop_directory(obj, f"{directory_path}/{obj.GetName()}")
            elif isinstance(obj, ROOT.TH1):
                # Compare the histograms
                hist_name = obj.GetName()
                
                # Get the histograms from both files
                hist1 = file1.Get(f"{directory_path}/{hist_name}")
                hist2 = file2.Get(f"{directory_path}/{hist_name}")

                # Check if the histograms have the same number of bins
                if hist1.GetNbinsX() != hist2.GetNbinsX():
                    print(f"Histogram {hist_name} has a different number of bins in the two files")
                    continue

                # Check if the histograms have the same bin edges
                for i in range(hist1.GetNbinsX()+1):
                    if hist1.GetBinLowEdge(i) != hist2.GetBinLowEdge(i):
                        print(f"Histogram {hist_name} has different bin edges in the two files")
                        break

                # Check if the histograms have the same bin contents and weights
                diff = False
                for i in range(hist1.GetNbinsX()):
                    if hist1.GetBinContent(i+1) != hist2.GetBinContent(i+1):
                        different_histograms.append(hist_name)
                        print(f"Histogram {hist_name} has different bin contents in the two files:")
                        print(f"  {hist1.GetBinContent(i+1)} vs {hist2.GetBinContent(i+1)} ({hist1.GetBinContent(i+1) / hist2.GetBinContent(i+1):.2f})")
                        diff = True
                        break
                    if hist1.GetBinError(i+1) != hist2.GetBinError(i+1):
                        print(f"Histogram {hist_name} has different bin weights in the two files")
                        break
                if not diff:
                    equivalent_histograms.append(hist_name)

    # Loop over all top-level directories in the first file
    for key in file1.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TDirectory):
            # Recursively loop over all histograms in the directory
            loop_directory(obj, obj.GetName())

    print(f"Equivalent histograms: {equivalent_histograms}")
    print(f"Different histograms: {different_histograms}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('unnormalized_histos', type=str)
    parser.add_argument('normalized_histos', type=str)

    args = parser.parse_args()

    unnormalized_histo_path = [f for f in sorted(Path(args.unnormalized_histos).glob('*.root'))][0]
    normalized_histo_path = [f for f in sorted(Path(args.normalized_histos).glob('*.root'))][0]

    unnormalized_tfile = ROOT.TFile(str(unnormalized_histo_path))
    normalized_tfile = ROOT.TFile(str(normalized_histo_path))

    compare_tfile_weights(unnormalized_tfile, normalized_tfile)


if __name__ == "__main__":
    main()