#!/usr/bin/env python
import os
from os import path
from sigXsec_1lep import *
from ROOT import *
import argparse
from datetime import datetime

today = datetime.date(datetime.now())
filepath = os.getcwd()

#Setting up ATLAS style
dirpath = os.path.dirname(os.path.realpath(__file__))
gROOT.SetBatch()
gROOT.LoadMacro('{}/AtlasStyle.C'.format(dirpath))
gROOT.LoadMacro('{}/AtlasUtils.C'.format(dirpath))
SetAtlasStyle()

parse = argparse.ArgumentParser()
parse.add_argument('--indir',           type=str,   default="statResults_tt1lep_%s"%today,
                    help='directory of the input root (limit) files')
parse.add_argument('--outdir',          type=str,   default="masslimit_%s"%today,
                    help='plots will be saved here, under plots dir')
parse.add_argument("--JESconfig",      type=str,   default="category",
                    help="JES configurations to be used: 'global' or 'category'")
parse.add_argument('--SR',              type=str,   default="combined",
                    help='signal region: combined, b1SR, b2SR')
parse.add_argument("--suff",           type=str,  default="",
                    help="suffix added to the outdir and configdir")
parse.add_argument("--drawStatOnly",  default=True,  action='store_true',
                    help="use --drawStatOnly if you want to make plots the stat-only line")


args            = parse.parse_args()
JESconfig       = args.JESconfig
indir           = args.indir+'_'+args.suff
outdir          = args.outdir+'_'+args.suff
SR              = args.SR
suff            = args.suff
drawStatOnly    = args.drawStatOnly

print ("=====================================================================")
print ("INPUTS to the SCRIPT: ")
print ("=====================================================================")
print ("indir                : ", indir)
print ("outdir               : ", outdir)
print ("JESconfig            : ", JESconfig)
print ("SR                   : ", SR)
print ("suff                 : ", suff)
print ("drawStatOnly         : ", drawStatOnly)
print ("=====================================================================")


suff = ''
if drawStatOnly:
    suff    = '_wStatOnly'

if SR == "combined":
  suffix_SR = ""
elif SR == "resolved":
  suffix_SR = "resolved"
elif SR == "boosted":
  suffix_SR = "boosted"



outpath = filepath+'/plots/'+outdir+'_'+JESconfig+'JES_BLIND/'
os.system('mkdir -p %s'%outpath)

gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

clim = TCanvas("clim", "", 1000, 700);
if drawStatOnly:
    l = TLegend(0.5,0.60,0.89,0.85)
else:
    l = TLegend(0.44,0.70,0.89,0.91)
l.SetBorderSize(0)
l.SetTextSize(0.03)
l.SetTextFont(42)
#clim.SetGridx()
#clim.SetGridy()

h = TH1F("h", "", 13, 0.40, 5.5);
#h.GetYaxis().SetRangeUser(1e-4, 20);
h.GetYaxis().SetRangeUser(5*1e-4, 500);
h.GetYaxis().SetTitle("#sigma(pp #rightarrow Z') #times B(Z' #rightarrow t#bar{t}) [pb]");
h.GetXaxis().SetTitle("m_{Z'} [TeV]");
h.GetXaxis().SetTitleOffset(1.3);
h.GetXaxis().SetLabelSize(0.05);
h.GetXaxis().SetTitleSize(0.05);
h.Draw("hist");

length =len(signalList)-1
xsec = TGraph(length);
exp = TGraph(length);
obs = TGraph(length);
exp_statonly = TGraph(length);
sigma1 = TGraphAsymmErrors(length);
sigma2 = TGraphAsymmErrors(length);
idx=0

for i in signalList:

    f = TFile(filepath+"/run/"+indir+"/allsys/"+i+"/Limits/asymptotics/"+i+suffix_SR+"_BLIND_CL95.root")
    allsys_tree = f.stats
    for ev in range(allsys_tree.GetEntries()):
        allsys_tree.GetEntry(ev)
        muobs = getattr(allsys_tree,'obs_upperlimit')
        muexp = getattr(allsys_tree,'exp_upperlimit')
        exp_p2 = getattr(allsys_tree,'exp_upperlimit_plus2')
        exp_p1 = getattr(allsys_tree,'exp_upperlimit_plus1')
        exp_m2 = getattr(allsys_tree,'exp_upperlimit_minus2')
        exp_m1 = getattr(allsys_tree,'exp_upperlimit_minus1')

        muexp_p2 = abs(-muexp + exp_p2)
        muexp_p1 = abs(-muexp + exp_p1)
        muexp_m1 = abs(-muexp + exp_m1)
        muexp_m2 = abs(-muexp + exp_m2)
    
    f_statonly = TFile(filepath+"/run/"+indir+"/statonly/"+i+"/Limits/asymptotics/"+i+"_statonly_BLIND_CL95.root")
    statonly_tree = f_statonly.stats
    for ev in range(statonly_tree.GetEntries()):
        statonly_tree.GetEntry(ev)
        muobs_statonly = getattr(statonly_tree,'obs_upperlimit')
        muexp_statonly = getattr(statonly_tree,'exp_upperlimit')
        exp_p2_statonly = getattr(statonly_tree,'exp_upperlimit_plus2')
        exp_p1_statonly = getattr(statonly_tree,'exp_upperlimit_plus1')
        exp_m2_statonly = getattr(statonly_tree,'exp_upperlimit_minus2')
        exp_m1_statonly = getattr(statonly_tree,'exp_upperlimit_minus1')

        muexp_p2_statonly = abs(-muexp_statonly + exp_p2_statonly)
        muexp_p1_statonly = abs(-muexp_statonly + exp_p1_statonly)
        muexp_m1_statonly = abs(-muexp_statonly + exp_m1_statonly)
        muexp_m2_statonly = abs(-muexp_statonly + exp_m2_statonly)


    ftxt = open(outpath+'limit_'+i+'_limitBLIND.txt', 'w')
    ftxt.write('muobs     '+str(muobs)+'\n')
    ftxt.write('muexp     '+str(muexp)+'\n')
    ftxt.write('muexp_statonly     '+str(muexp_statonly)+'\n')
    ftxt.write('muexp_p2  '+str(muexp_p2)+'\n')
    ftxt.write('muexp_p1  '+str(muexp_p1)+'\n')
    ftxt.write('muexp_m1  '+str(muexp_m1)+'\n')
    ftxt.write('muexp_m2  '+str(muexp_m2)+'\n')
    ftxt.write('xsec      '+str(xs[i])+'\n')
    ftxt.close()
    print( mass[i],"TeV\tlimits in pb, exp: %10f (1 sigma: +%10f -%10f), (2 sigma: +%10f -%10f)\tobs: %10f" % (muexp*xs[i], muexp_p1*xs[i], muexp_m1*xs[i], muexp_p2*xs[i], muexp_m2*xs[i], muobs*xs[i]))
    sigma1.SetPoint(idx, mass[i], muexp*xs[i])
    sigma1.SetPointError(idx, 0, 0, muexp_m1*xs[i], muexp_p1*xs[i])
    sigma2.SetPoint(idx, mass[i], muexp*xs[i])
    sigma2.SetPointError(idx, 0, 0, muexp_m2*xs[i], muexp_p2*xs[i])
    xsec.SetPoint(idx, mass[i], xs[i])
    exp.SetPoint(idx, mass[i], muexp*xs[i])
    exp_statonly.SetPoint(idx, mass[i], muexp_statonly*xs[i])
    obs.SetPoint(idx, mass[i], muobs*xs[i])
    idx += 1

exp.SetLineWidth(2);
obs.SetLineWidth(2);
exp.SetMarkerStyle(20);
obs.SetMarkerStyle(20);
exp.SetMarkerSize(1.0);
obs.SetMarkerSize(1.0);
obs.SetMarkerColor(kMagenta);
obs.SetLineColor(kBlack);
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
exp_statonly.SetLineWidth(2);
exp_statonly.SetLineStyle(2);

l.AddEntry(exp, "Expected 95% CL upper limit", "L")
if drawStatOnly:
    l.AddEntry(exp_statonly, "Expected 95% CL upper limit (stat-only)", "L")
l.AddEntry(sigma1, "Expected 95% CL upper limit #pm 1 #sigma", "F")
l.AddEntry(sigma2, "Expected 95% CL upper limit #pm 2 #sigma", "F")
l.AddEntry(xsec, "LO Z'_{TC2}(#Gamma/m=1.2%) cross-section #times 1.3", "L")

sigma2.Draw("3");
sigma1.Draw("3");
exp.Draw("LP")
#obs.Draw("LP")
if drawStatOnly:
    exp_statonly.Draw("L")
xsec.Draw("L")
l.Draw()
clim.SetLogy(1)

gPad.RedrawAxis()

def stampText(x, y, text, size):
    t = TLatex()
    t.SetNDC()
    #t.SetTextAlign(13)
    t.SetTextFont(42)
    t.SetTextColor(kBlack)
    t.SetTextSize(size)
    t.DrawLatex(x,y, text)

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

stampATLAS("Internal", 0.2, 0.88)
stampLumiText(139, 0.2, 0.83, "#sqrt{s} = 13 TeV", 0.04)
if SR == "resolved":
    stampText(0.2, 0.77, "Resolved SRs only", 0.04)
elif SR == "boosted":
    stampText(0.2, 0.77, "Boosted SRs only", 0.04)

for i in ['.eps', '.png', '.pdf']:
    clim.SaveAs(outpath+"massLimit_%s_%s%s"%(SR,suff,i))

i=0

for i in range(3000, 5000, 1):
    #print i, xsec.Eval(i/1000.0), exp.Eval(i/1000.0)
    if 10000*xsec.Eval(i/1000.0) < 10000*exp.Eval(i/1000.0):
    #if 10000*(exp.Eval(i/1000.0) - xsec.Eval(i/1000.0)) > 1e-8:
        print ("======================================")
        print ("\033[31;1mThe expected limit is %s GeV\033[0m"%i)
        print ("======================================")
        break


fout = TFile(outpath+"/massLimit_%s_%s.root"%(SR,suff),"RECREATE")
xsec.Write("theory")
exp.Write("expected")
obs.Write("observed")
exp_statonly.Write("statonly")
sigma1.Write("exp_sigma1")
sigma2.Write("exp_sigma2")
xsec.Write()

