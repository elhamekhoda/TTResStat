#!/usr/bin/env python
import os
from os import path
import sys
from ROOT import *
import argparse
from datetime import datetime
from pathlib import Path
import json

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


def plot_limits(dir_1l, dir_2l, dir_combined):
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
    with open(path.join(dir_combined, 'settings.json')) as f:
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

    out_dir = Path(dir_combined) / 'plots'
    out_dir.mkdir(exist_ok=True)

    clim = TCanvas("clim", "", 1000, 700)

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

    limit_files_1l = [l for l in Path(dir_1l / 'limits').glob('*.root')]
    limit_files_2l = [l for l in Path(dir_2l / 'limits').glob('*.root')]
    limit_files_comb = [l for l in Path(dir_combined / 'limits').glob('*.root')]

    def get_mass(filename):
        return int(filename.stem.split('_')[0].replace(signal_name, ''))

    limit_files_1l.sort(key=get_mass)
    limit_files_2l.sort(key=get_mass)
    limit_files_comb.sort(key=get_mass)
    # remove mass = 500 from lists
    # limit_files_2l = limit_files_2l[1:]
    # limit_files_comb = limit_files_comb[1:]


    

    length = len(limit_files_comb)
    xsec = TGraph(length)
    exp_1l = TGraph(length)
    exp_2l = TGraph(length)
    exp_comb = TGraph(length)

    for exp, limit_files in zip([exp_1l, exp_2l, exp_comb], [limit_files_1l, limit_files_2l, limit_files_comb]):
        idx = 0
        for limit_file in limit_files:
            m = get_mass(limit_file)
            outname = settings['signal'] + str(m)
            f = TFile(str(limit_file))
            tree = f.stats
            for ev in range(tree.GetEntries()):
                tree.GetEntry(ev)
                muexp = getattr(tree, 'exp_upperlimit')
            cross_section = xs[outname]
            m_tev = m / 1000.
            xsec.SetPoint(idx, m_tev, cross_section)
            exp.SetPoint(idx, m_tev, muexp*cross_section)
            idx += 1

    xsec.SetLineWidth(3)
    xsec.SetLineColor(kRed)
    for exp, color, style in zip([exp_1l, exp_2l, exp_comb], [kBlack, kBlue, 28], [kSolid, kDotted, kDotted]):
        exp.SetLineColor(color)
        exp.SetLineStyle(style)
        exp.SetLineWidth(2)
        exp.SetMarkerStyle(20)
        exp.SetMarkerSize(1.0)
        # exp.Draw("l same")
        exp.Draw("LP")


    l.AddEntry(exp_1l, "Expected 95% CL upper limit (orig)", "L")
    l.AddEntry(exp_2l, "Expected 95% CL upper limit (merge btag)", "L")
    l.AddEntry(exp_comb, "Expected 95% CL upper limit (merge lepton)", "L")
    l.AddEntry(xsec, "LO theory cross-section", "L")

    xsec.Draw("L")
    l.Draw()
    clim.SetLogy(1)

    gPad.RedrawAxis()

    stampATLAS("Work in Progress", 0.2, 0.88)
    stampLumiText(139, 0.2, 0.83, "#sqrt{s} = 13 TeV", 0.04)

    for i in ['.eps', '.png', '.pdf']:
        clim.SaveAs(
            str(out_dir/f"{settings['signal']}_{settings['channel']}_limit_comparison{i}"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_original', type=Path)
    parser.add_argument('dir_merge_btag', type=Path)
    parser.add_argument('dir_merge_leptons', type=Path)

    args = parser.parse_args()
    plot_limits(args.dir_original, args.dir_merge_btag, args.dir_merge_leptons)


if __name__ == "__main__":
    main()
