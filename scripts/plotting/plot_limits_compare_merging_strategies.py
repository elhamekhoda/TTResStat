#!/usr/bin/env python
import os
from os import path
import sys
from ROOT import *
import argparse
from datetime import datetime
from pathlib import Path
import json
from array import array

from sigXsec_1lep import zprime_xs, grav_xs, gluon_xs

def stampATLAS(text, x, y):
    t = TLatex()
    t.SetNDC()
    t.SetTextFont(72)
    t.SetTextColor(1)
    delx = 0.115*696*gPad.GetWh()/(472*gPad.GetWw()) + 6*0.04
    t.SetTextSize(0.06)
    t.DrawLatex(x, y, "ATLAS Simulation")
    t.SetTextFont(42)
    t.SetTextSize(0.06)
    t.DrawLatex(x+delx, y, text)


def stampLumiText(lumi, x, y, text, size):
    t = TLatex()
    t.SetNDC()
    t.SetTextFont(42)
    t.SetTextColor(1)
    t.SetTextSize(size)
    # t.DrawLatex(x,y,"#int L dt = "+str(lumi)+" fb^{-1}, "+text)
    t.DrawLatex(x, y, text+", "+str(lumi)+" fb^{-1}")


def ratio_graph(graph1, graph2):
    # Create dictionaries of x:y for each graph
    x1_to_y1 = {graph1.GetX()[i]: graph1.GetY()[i] for i in range(graph1.GetN())}
    x2_to_y2 = {graph2.GetX()[i]: graph2.GetY()[i] for i in range(graph2.GetN())}

    # Create a list of (x, y) pairs where y is the ratio of y values for matching x in both graphs
    ratio_points = [(x1, y1 / x2_to_y2[x1]) for x1, y1 in x1_to_y1.items() if x1 in x2_to_y2 and x2_to_y2[x1] != 0]

    # Create the ratio graph
    ratio_graph_ = TGraph(len(ratio_points), array('d', [x for x, y in ratio_points]), array('d', [y for x, y in ratio_points]))

    return ratio_graph_

def draw_ratio_pad(ratio_pad, exp_original, graph1, graph2, graph3):
    ratio_pad.cd()
    ratio_pad.SetGridy()

    # Define the ratio graphs
    ratio_graph_1_0 = ratio_graph(graph1, exp_original)
    ratio_graph_2_0 = ratio_graph(graph2, exp_original)
    ratio_graph_3_0 = ratio_graph(graph3, exp_original)

    # Adjust y-axis range if needed
    min_y = min(ratio_graph_1_0.GetY())
    max_y = max(ratio_graph_1_0.GetY())

    # Create a frame to draw in the pad
    frame = ratio_pad.DrawFrame(0.50, min_y * 0.8, 5, max_y * 1.2)
    frame.GetXaxis().SetTitle("m_{Z'} [TeV]")
    frame.GetYaxis().SetTitle("Merge/Original")

    # Draw the ratio graphs
    for ratio_graph_ in [ratio_graph_1_0, ratio_graph_2_0, ratio_graph_3_0]:
        n_points = ratio_graph_.GetN()

        for i in range(n_points):
            x = ratio_graph_.GetX()[i]
            y = ratio_graph_.GetY()[i]
            print("x: {}, y: {}".format(x, y))
        ratio_graph_.Draw("same")

def plot_limits(original_dir, btag_dir, lepton_dir, btag_lepton_dir):
    # Setting up ATLAS style
    dirpath = os.path.dirname(os.path.realpath(__file__))
    gROOT.SetBatch()
    gROOT.LoadMacro('{}/AtlasStyle.C'.format(dirpath))
    gROOT.LoadMacro('{}/AtlasUtils.C'.format(dirpath))
    SetAtlasStyle()
    gStyle.SetOptStat(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

    # get args from json file
    with open(path.join(lepton_dir, 'settings.json')) as f:
        settings = json.load(f)

    if settings['signal'] == 'zprime':
        signal_name = 'ZprimeTC2'
        xs = zprime_xs
    elif settings['signal'] == 'grav':
        signal_name = 'Grav'
        xs = grav_xs
    elif settings['signal'] == 'gluon':
        signal_name = 'KKg'
        xs = gluon_xs
    else:
        raise NotImplementedError(
            'Signal {} not implemented'.format(settings['signal']))

    out_dir = Path(btag_lepton_dir) / 'plots'
    out_dir.mkdir(exist_ok=True)

    # clim = TCanvas("clim", "", 1000, 700)
    # Setting up the canvas
    clim = TCanvas("clim", "", 1000, 800)
    clim.Divide(1, 2)

    pad1 = clim.cd(1)
    pad1.SetPad(0.01, 0.25, 0.99, 0.99)
    pad1.SetLogy(1)
    pad1.SetBottomMargin(0)

    pad2 = clim.cd(2)
    pad2.SetPad(0.01, 0.01, 0.99, 0.24)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.25)

    # Move back to the main pad
    pad1.cd()

    l = TLegend(0.44, 0.65, 0.89, 0.85)
    l.SetBorderSize(0)
    l.SetTextSize(0.03)
    l.SetTextFont(42)

    if settings['signal'] == 'zprime':
        h = TH1F("h", "", 12, 0.50, 5)
    elif settings['signal'] == 'grav':
        h = TH1F("h", "", 12, 0.50, 3.)
    elif settings['signal'] == 'gluon':
        h = TH1F("h", "", 12, 0.50, 5)
    # h.GetYaxis().SetRangeUser(1e-4, 20);
    h.GetYaxis().SetRangeUser(5*1e-4, 1e3)
    if settings['signal'] == 'zprime':
        h.GetYaxis().SetTitle(
            "#sigma(pp #rightarrow Z') #times B(Z' #rightarrow t#bar{t}) [pb]")
        h.GetXaxis().SetTitle("m_{Z'} [TeV]")
    elif settings['signal'] == 'grav':
        h.GetYaxis().SetTitle(
            "#sigma(pp #rightarrow G_{KK}) #times B(G_{KK} #rightarrow t#bar{t}) [pb]")
        h.GetXaxis().SetTitle("m_{G_{KK}} [TeV]")
    elif settings['signal'] == 'gluon':
        h.GetYaxis().SetTitle(
            "#sigma(pp #rightarrow g_{KK}) #times B(g_{KK} #rightarrow t#bar{t}) [pb]")
        h.GetXaxis().SetTitle("m_{g_{KK}} [TeV]")
    h.GetXaxis().SetTitleOffset(1.3)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitleSize(0.05)
    h.Draw("hist")

    limit_files_original = [l for l in Path(original_dir / 'limits').glob('*.root')]
    limit_files_btag = [l for l in Path(btag_dir / 'limits').glob('*.root')]
    limit_files_lepton = [l for l in Path(lepton_dir / 'limits').glob('*.root')]
    limit_files_btag_lepton = [l for l in Path(btag_lepton_dir / 'limits').glob('*.root')]

    def get_mass(filename):
        return int(filename.stem.split('_')[0].replace(signal_name, ''))

    limit_files_original.sort(key=get_mass)
    limit_files_btag.sort(key=get_mass)
    limit_files_lepton.sort(key=get_mass)
    limit_files_btag_lepton.sort(key=get_mass)
    

    length = len(limit_files_lepton)
    xsec = TGraph(length)
    exp_original = TGraph(length)
    exp_btag = TGraph(length)
    exp_lepton = TGraph(length)
    exp_btag_lepton = TGraph(length)

    for exp, limit_files in zip([exp_original, exp_btag, exp_lepton, exp_btag_lepton], [limit_files_original, limit_files_btag, limit_files_lepton, limit_files_btag_lepton]):
        idx = 0
        for limit_file in limit_files:
            m = get_mass(limit_file)
            outname = settings['signal'] + str(m)
            f = TFile(str(limit_file))
            tree = f.stats
            for ev in range(tree.GetEntries()):
                tree.GetEntry(ev)
                # muexp = getattr(tree, 'exp_upperlimit')
                muexp = getattr(tree, 'exp_upperlimit')
                # exp_p2 = getattr(tree, 'exp_upperlimit_plus2')
                # exp_p1 = getattr(tree, 'exp_upperlimit_plus1')
                # exp_m2 = getattr(tree, 'exp_upperlimit_minus2')
                exp_m1 = getattr(tree, 'exp_upperlimit_minus1')

                # muexp_p2 = abs(-muexp + exp_p2)
                muexp_m1 = abs(-muexp + exp_m1)
                muexp = muexp_m1
            cross_section = xs[outname]
            m_tev = m / 1000.
            xsec.SetPoint(idx, m_tev, cross_section)
            exp.SetPoint(idx, m_tev, muexp*cross_section)
            idx += 1

    xsec.SetLineWidth(3)
    xsec.SetLineColor(kRed)
    for exp, color, style in zip([exp_original, exp_btag, exp_lepton, exp_btag_lepton], [kBlack, kBlue, 28, 35], [kSolid, kDotted, kDotted, kDashed]):
        exp.SetLineColor(color)
        exp.SetLineStyle(style)
        exp.SetLineWidth(2)
        exp.SetMarkerStyle(20)
        exp.SetMarkerSize(1.0)
        # exp.Draw("l same")
        exp.Draw("LP")


    l.AddEntry(exp_original, "Expected 95% CL upper limit -1 #sigma (orig)", "L")
    l.AddEntry(exp_btag, "Expected 95% CL upper limit -1 #sigma (merge btag)", "L")
    l.AddEntry(exp_lepton, "Expected 95% CL upper limit -1 #sigma (merge lepton)", "L")
    l.AddEntry(exp_btag_lepton, "Expected 95% CL upper limit -1 #sigma (merge btag+lepton)", "L")
    l.AddEntry(xsec, "LO theory cross-section", "L")

    xsec.Draw("L")
    l.Draw()
    # clim.SetLogy(1)
    stampATLAS("Work in Progress", 0.2, 0.88)
    stampLumiText(139, 0.2, 0.83, "#sqrt{s} = 13 TeV", 0.04)

    draw_ratio_pad(pad2, exp_original, exp_btag, exp_lepton, exp_btag_lepton)

    gPad.RedrawAxis()

    

    for i in ['.eps', '.png', '.pdf']:
        clim.SaveAs(
            str(out_dir/f"{settings['signal']}_{settings['channel']}_limit_comparison{i}"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_original', type=Path)
    parser.add_argument('dir_merge_btag', type=Path)
    parser.add_argument('dir_merge_leptons', type=Path)
    parser.add_argument('dir_merge_btag_leptons', type=Path)

    args = parser.parse_args()
    plot_limits(args.dir_original, args.dir_merge_btag, args.dir_merge_leptons, args.dir_merge_btag_leptons)


if __name__ == "__main__":
    main()
