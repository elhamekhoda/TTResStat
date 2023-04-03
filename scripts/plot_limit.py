#!/usr/bin/env python
import os
from os import path
from sigXsec_1lep import *
from ROOT import *
import argparse
from datetime import datetime
from pathlib import Path
import json

def stampATLAS(text, x, y):
    t = TLatex()
    t.SetNDC()
    t.SetTextFont(72)
    t.SetTextColor(1)
    delx = 0.115*696*gPad.GetWh()/(472*gPad.GetWw()) + 0.04
    t.SetTextSize(0.06)
    t.DrawLatex(x,y,"ATLAS")
    t.SetTextFont(42)
    t.SetTextSize(0.06)
    t.DrawLatex(x+delx, y, text)

def stampLumiText(lumi, x, y, text, size):
    t = TLatex()
    t.SetNDC()
    t.SetTextFont(42)
    t.SetTextColor(1)
    t.SetTextSize(size)
    #t.DrawLatex(x,y,"#int L dt = "+str(lumi)+" fb^{-1}, "+text)
    t.DrawLatex(x,y, text+", "+str(lumi)+" fb^{-1}")

def plot_limits(run_dir):
    #Setting up ATLAS style
    dirpath = os.path.dirname(os.path.realpath(__file__))
    gROOT.SetBatch()
    gROOT.LoadMacro('{}/AtlasStyle.C'.format(dirpath))
    gROOT.LoadMacro('{}/AtlasUtils.C'.format(dirpath))
    SetAtlasStyle()
    gStyle.SetOptStat(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

    # get args from json file
    with open(path.join(run_dir, 'settings.json')) as f:
        settings = json.load(f)

    if settings['signal'] == 'zprime':
        signal_name = 'ZprimeTC2'
    elif settings['signal'] == 'grav':
        raise NotImplementedError('Graviton not implemented yet')
    else:
        raise NotImplementedError('Signal {} not implemented'.format(settings['signal']))
    
    limit_dir = Path(run_dir) / 'limits'
    out_dir = Path(run_dir) / 'plots'
    out_dir.mkdir(exist_ok=True)

    clim = TCanvas("clim", "", 1000, 700);

    l = TLegend(0.44,0.65,0.89,0.85)
    l.SetBorderSize(0)
    l.SetTextSize(0.03)
    l.SetTextFont(42)
    #clim.SetGridx()
    #clim.SetGridy()

    h = TH1F("h", "", 12, 0.50, 5.5);
    #h.GetYaxis().SetRangeUser(1e-4, 20);
    h.GetYaxis().SetRangeUser(5*1e-4, 100);
    h.GetYaxis().SetTitle("#sigma(pp #rightarrow Z') #times B(Z' #rightarrow t#bar{t}) [pb]");
    h.GetXaxis().SetTitle("m_{Z'} [TeV]");
    h.GetXaxis().SetTitleOffset(1.3);
    h.GetXaxis().SetLabelSize(0.05);
    h.GetXaxis().SetTitleSize(0.05);
    h.Draw("hist");



    limit_files = [l for l in limit_dir.glob('*.root')]
    def get_mass(filename):
        return int(filename.stem.split('_')[0].replace(signal_name, ''))
    limit_files.sort(key=get_mass)

    length =len(limit_files)
    xsec = TGraph(length);
    exp = TGraph(length);
    #obs = TGraph(length);
    exp_statonly = TGraph(length);
    sigma1 = TGraphAsymmErrors(length);
    sigma2 = TGraphAsymmErrors(length);
    idx=0

    for limit_file in limit_files:
        m = get_mass(limit_file)
        outname = settings['signal'] + str(m)
        f = TFile(str(limit_file))
        tree = f.stats
        for ev in range(tree.GetEntries()):
            tree.GetEntry(ev)
            #muobs = getattr(tree,'obs_upperlimit')
            muexp = getattr(tree,'exp_upperlimit')
            exp_p2 = getattr(tree,'exp_upperlimit_plus2')
            exp_p1 = getattr(tree,'exp_upperlimit_plus1')
            exp_m2 = getattr(tree,'exp_upperlimit_minus2')
            exp_m1 = getattr(tree,'exp_upperlimit_minus1')

            muexp_p2 = abs(-muexp + exp_p2)
            muexp_p1 = abs(-muexp + exp_p1)
            muexp_m1 = abs(-muexp + exp_m1)
            muexp_m2 = abs(-muexp + exp_m2)

        ftxt = open(out_dir/('limit_'+outname+'_limitBLIND.txt'), 'w')
        #ftxt.write('muobs     '+str(muobs)+'\n')
        ftxt.write('muexp     '+str(muexp)+'\n')
        ftxt.write('muexp_p2  '+str(muexp_p2)+'\n')
        ftxt.write('muexp_p1  '+str(muexp_p1)+'\n')
        ftxt.write('muexp_m1  '+str(muexp_m1)+'\n')
        ftxt.write('muexp_m2  '+str(muexp_m2)+'\n')
        cross_section = xs[outname]
        ftxt.write('xsec      '+str(cross_section)+'\n')
        ftxt.close()
        print (mass[outname],"TeV\tlimits in pb, exp: %10f (1 sigma: +%10f -%10f), (2 sigma: +%10f -%10f)" % (muexp*cross_section, muexp_p1*cross_section, muexp_m1*cross_section, muexp_p2*cross_section, muexp_m2*cross_section))
        sigma1.SetPoint(idx, mass[outname], muexp*cross_section)
        sigma1.SetPointError(idx, 0, 0, muexp_m1*cross_section, muexp_p1*cross_section)
        sigma2.SetPoint(idx, mass[outname], muexp*cross_section)
        sigma2.SetPointError(idx, 0, 0, muexp_m2*cross_section, muexp_p2*cross_section)
        xsec.SetPoint(idx, mass[outname], cross_section)
        exp.SetPoint(idx, mass[outname], muexp*cross_section)
        #obs.SetPoint(idx, mass[outname], muobs*cross_section)
        idx += 1

    exp.SetLineWidth(2);
    #obs.SetLineWidth(2);
    exp.SetMarkerStyle(20);
    #obs.SetMarkerStyle(20);
    exp.SetMarkerSize(1.0);
    #obs.SetMarkerSize(1.0);
    #obs.SetMarkerColor(kMagenta);
    #obs.SetLineColor(kBlack);
    xsec.SetLineWidth(3);
    xsec.SetLineColor(kRed);
    sigma2.SetFillStyle(1001);
    sigma2.SetFillColor(5);
    sigma2.SetLineColor(5);
    sigma2.SetMarkerColor(5);
    sigma1.SetFillStyle(1001);
    sigma1.SetFillColor(3);
    sigma1.SetMarkerColor(3);
    sigma1.SetLineColor(3);

    exp.SetMarkerColor(kBlue);
    exp.SetLineColor(kBlue);

    l.AddEntry(exp, "Expected 95% CL upper limit", "L")
    #l.AddEntry(obs, "Observed 95% CL upper limit (stat-only)", "L")
    l.AddEntry(sigma1, "Expected 95% CL upper limit #pm 1 #sigma", "F")
    l.AddEntry(sigma2, "Expected 95% CL upper limit #pm 2 #sigma", "F")
    l.AddEntry(xsec, "LO Z'_{TC2}(#Gamma/m=1.2%) cross-section #times 1.3", "L")

    sigma2.Draw("3");
    sigma1.Draw("3");
    exp.Draw("LP")
    xsec.Draw("L")
    #obs.Draw("L")
    l.Draw()
    clim.SetLogy(1)

    gPad.RedrawAxis()

    stampATLAS("Work in Progress", 0.2, 0.88)
    stampLumiText(139, 0.2, 0.83, "#sqrt{s} = 13 TeV", 0.04)

    for i in ['.eps', '.png', '.pdf']:
        clim.SaveAs(str(out_dir/("mass_limit%s"%(i))))

    i=0

    for i in range(3000, 5000, 1):
        #print i, xsec.Eval(i/1000.0), exp.Eval(i/1000.0)
        if 10000*xsec.Eval(i/1000.0) < 10000*exp.Eval(i/1000.0):
        #if 10000*(exp.Eval(i/1000.0) - xsec.Eval(i/1000.0)) > 1e-8:
            print ("======================================")
            print ("\033[31;1mThe expected limit is %s GeV\033[0m"%i)
            print ("======================================")
            break


    fout = TFile(str(out_dir/("mass_limit.root")),"RECREATE")
    xsec.Write("theory")
    exp.Write("expected")
    #obs.Write("observed")
    exp_statonly.Write("statonly")
    sigma1.Write("exp_sigma1")
    sigma2.Write("exp_sigma2")
    xsec.Write()




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('run_dir', help='the input run directory')

    args = parser.parse_args()
    plot_limits(args.run_dir)


if __name__ == "__main__":
    main()





