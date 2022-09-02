

import json
from collections import OrderedDict
from ROOT import *
import os
import sys
import argparse
from systematics_List_1lep import *
# sys.path.insert(0, '/home/elham/statanalysis_ttres1lep/scripts/')
from systematics import *

# with open('filenames.json') as f:
#   data = json.load(f)


# print(data["mc16e"].keys())
# print(data["mc16e"]["filepath"])
# print(data["mc16e"]["tt"]["periodFraction"])

LUMI = OrderedDict((
('2015', dict(lumi=3.21956)),
('2016', dict(lumi=32.9881)),
('2017', dict(lumi=44.3074)),
('2018', dict(lumi=58.4501)))
)


def get_lumi(*periods):
    lumi = 0
    for p in periods:
        for pp in p.split('+'):
            lumi += LUMI[pp.strip()]['lumi']
    return lumi

def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))  # or return list(set(list1) ^ set(list2))

class dataset:
    def __init__ (self, data, campaign, sample, variables):
        self.name = sample
        self.filename = data[campaign][sample]["name"]
        self.periodFraction = data[campaign][sample]["periodFraction"]
        self.lumi = data[campaign][sample]["lumi"]
        self.variables = variables
        self.excld_syst = data[campaign][sample]["exclude_sys"]
        self.filepath = data[campaign]["filepath"]



def parse_json(json_file, campaign, sample, variables):
    with open('%s.json' % json_file) as f:
        data = json.load(f)
    sample_list = diff(data[campaign].keys(),['filepath'])
    if sample not in sample_list:
        raise NameError('\033[31;1m sample %s is not included in the samples list\033[0m' % sample)
    sample_obj = dataset(data, campaign, sample, variables)

    return sample_obj


def create_limit_inputs(sample, sysVar_list, periodfrac, outpath):
    print "\033[42;1m =======> Producing files for %s \033[0m" % sample.name

    if sample.name in ["data", "qcd"]:
        scale = 1.0
    else:
        scale = periodfrac*139.0*1000/float(sample.periodFraction)

    if sample.name == "data":
        sysVar_list = ['']
    elif sample.excld_syst in ["all", "All", "ALL"]:
        sysVar_list = ['']
        print "\033[34;1m All Systematics are ignored for %s \033[0m" % sample.name
    # elif sample.excld_syst not in ["all", "All", "ALL", "none", "None", "NONE"]:
    #     sysVar_list = diff(sysVar_list,list(sample.excld_syst))

    for reg in ["be", "bmu", "re", "rmu"]:
        outdir = outpath +"/limit_inputs/"+reg+"/"
        comd = "mkdir -p "+outdir
        os.system(comd)

        filename = sample.filename
        filename = filename.replace("be", reg)
        print "Reading file: %s"%(sample.filepath + filename)

        inFile = TFile(sample.filepath+filename,'READ')
        outFile = TFile('%s/hist_%s.root'%(outdir,sample.name),'RECREATE')
        for syst in sysVar_list:
            tree1 = eval('inFile.mini'+syst)

            hmtt = {}; hmttPos = {}; hmttNeg = {}
            hmtt[syst,reg] = TH1F('mtt_tree_%s_%s'%(syst,reg),'', 6000, 0, 6000)
            # hmttPos[syst,reg] = TH1F('mttPos_tree_%s_%s'%(syst,reg),'', 6000, 0, 6000)
            # hmttNeg[syst,reg] = TH1F('mttNeg_tree_%s_%s'%(syst,reg),'', 6000, 0, 6000)
            tree1.Draw("mttReco>>{}".format(hmtt[syst,reg].GetName()), "w")
            # tree1.Draw("mttReco>>{}".format(hmttPos[syst,reg].GetName()), "(lep_charge==1)*w")
            # tree1.Draw("mttReco>>{}".format(hmttNeg[syst,reg].GetName()), "(lep_charge==-1)*w")
            for btag_cat in range(4):
                hmtt[syst,reg+str(btag_cat)] = TH1F('mtt_tree_%s_%s%s'%(syst,reg,str(btag_cat)),'', 6000, 0, 6000)
                # hmttPos[syst,reg+str(btag_cat)] = TH1F('mttPos_tree_%s_%s%s'%(syst,reg,str(btag_cat)),'', 6000, 0, 6000)
                # hmttNeg[syst,reg+str(btag_cat)] = TH1F('mttNeg_tree_%s_%s%s'%(syst,reg,str(btag_cat)),'', 6000, 0, 6000)
                tree1.Draw("mttReco>>{}".format(hmtt[syst,reg+str(btag_cat)].GetName()), "(Btagcat=={})*w".format(btag_cat))
                # tree1.Draw("mttReco>>{}".format(hmttPos[syst,reg+str(btag_cat)].GetName()), "(Btagcat=={})*(lep_charge==1)*w".format(btag_cat))
                # tree1.Draw("mttReco>>{}".format(hmttNeg[syst,reg+str(btag_cat)].GetName()), "(Btagcat=={})*(lep_charge==-1)*w".format(btag_cat))

            outFile.cd()
            hmtt[syst,reg].Scale(scale)
            # hmttPos[syst,reg].Scale(scale)
            # hmttNeg[syst,reg].Scale(scale)

            hmtt[syst,reg].Write("mtt"+syst)
            # hmttPos[syst,reg].Write("mttPos"+syst)
            # hmttNeg[syst,reg].Write("mttNeg"+syst)

            for btag_cat in range(4):
                hmtt[syst,reg+str(btag_cat)].Scale(scale)
                # hmttPos[syst,reg+str(btag_cat)].Scale(scale)
                # hmttNeg[syst,reg+str(btag_cat)].Scale(scale)

                # h_tmp = hmttPos[syst,reg+str(btag_cat)].Clone("mttAsym")
                # h_tmp.Add(hmttNeg[syst,reg+str(btag_cat)], -1)
                hmtt[syst,reg+str(btag_cat)].Write("mtt"+"_"+reg+str(btag_cat)+syst)
                # hmttPos[syst,reg+str(btag_cat)].Write("mttPos"+"_"+reg+str(btag_cat)+syst)
                # hmttNeg[syst,reg+str(btag_cat)].Write("mttNeg"+"_"+reg+str(btag_cat)+syst)
                # h_tmp.Write("mttAsym"+"_"+reg+str(btag_cat)+syst)
                # del h_tmp
        outFile.Close()


def extract_variables(sample, systlist, periodfrac, outpath):

    print "\033[42;1m =======> Producing files for %s \033[0m" % sample.name

    h1 = {}; h1_up = {}; h1_down = {}
    
    if sample.name in ["data", "qcd"]:
        scale = 1.0
    else:
        scale = periodfrac/float(sample.periodFraction)
        print scale


    if sample.name == "data":
        systlist = ['']
    elif sample.excld_syst in ["all", "All", "ALL"]:
        systlist = ['']
        print "\033[34;1m All Systematics are ignored for %s \033[0m" % sample.name
    elif sample.excld_syst not in ["all", "All", "ALL", "none", "None", "NONE"]:
        systlist = diff(systlist,list(sample.excld_syst))

    for reg in ["be", "bmu", "re", "rmu"]:
        filename = sample.filename
        filename = filename.replace("be", reg)
        print "Reading file: %s"%(sample.filepath + filename)

        inFile = TFile(sample.filepath+filename,'READ')
        outFile = TFile('%s/%s_%s.root'%(outpath,reg,sample.name),'RECREATE')

        for v in sample.variables:
            # print "Variable Name: ", v
            for sys in systlist:
                # print sys
                inFile.cd()
                if sys != '' and ("pdf" not in sys) and ("SoftTrk_Reso" not in sys):
                    h1_up[v] = inFile.Get(v+sys+'__1up')
                    h1_down[v] = inFile.Get(v+sys+'__1down')
                    h1_up[v].Scale(scale)
                    h1_down[v].Scale(scale)
                elif ("SoftTrk_Reso" in sys) or ("pdf" in sys):
                    h1_up[v] = inFile.Get(v+sys)
                    h1_up[v].Scale(scale)
                else:
                    h1[v] = inFile.Get(v)
                    h1[v].Scale(scale)
                outFile.cd()
                if sys != '' and ("pdf" not in sys) and ("SoftTrk_Reso" not in sys):
                    h1_up[v].Write(v+sys+'__1up')
                    h1_down[v].Write(v+sys+'__1down')
                elif ("SoftTrk_Reso" in sys) or ("pdf" in sys):
                    h1_up[v].Write(v+sys)
                else:
                    h1[v].Write(v)
        outFile.Close()
        inFile.Close()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign",    type=str,  default="mc16e",
                        help="MC campaign or the year of data taking. Options: mc16a, mc16d, mc16e")
    parser.add_argument("--outpath",       type=str,  default="./",
                        help="The path to the output files")
    parser.add_argument("--runSys", dest="runSys", default=True, action='store_true',
                        help="--runSys if you want to run over the systematics")
    args = parser.parse_args()

    campaign        = args.campaign
    outpath         = args.outpath+"/%s/"%campaign
    runSys          = args.runSys

    print "====================================================================="
    print "INPUTS to the SCRIPT: "
    print "====================================================================="
    print "campaign             : ", campaign
    print "outpath              : ", outpath
    print "runSys               : ", runSys
    print "====================================================================="


    # campaign = 'mc16e'
    # outpath = "/home/elham/ttResTools_june2021/run/tt1lep_02nov2021/"
    # runSys = True

    # Create the output folder
    comd = "mkdir -p "+outpath
    os.system(comd)

    # List of the processes
    # process_list = [ 'wjets', 'zjets', 'vv', 'singletop', 'ttV', 'qcd', 'data', "zprime400", "zprime500", "zprime750", "zprime1000", "zprime1250", "zprime1500", "zprime1750", "zprime2000", "zprime2250", "zprime2500", "zprime2750", "zprime30    00", "zprime4000", "zprime5000"]
    # process_list = ["qcd", "data","zprime400", "zprime500", "zprime750", "zprime1000", "zprime1250", "zprime1500", "zprime1750", "zprime2000", "zprime2250", "zprime2500", "zprime2750", "zprime3000", "zprime4000", "zprime5000"]
    # process_list = ["zprime2000", "zprime2250", "zprime2500", "zprime2750", "zprime3000", "zprime4000", "zprime5000"]
    # process_list = ['wjets', 'zjets', 'vv', 'singletop', 'qcd', 'data']
    process_list = ["wjets"] #"tt_af2", "tt_had", "tt_hs", "tt_hdamp"

    period_map = {
    "mc16a": "2015+2016",
    "mc16d": "2017",
    "mc16e": "2018"
    }
    PERIODS = ['2015+2016', '2017', '2018']
    PERIODS_TO_RUN = period_map[campaign]
    PFrac = get_lumi(PERIODS_TO_RUN)/get_lumi(*PERIODS)


    if runSys:
        all_sys = ['']+ syslist
    else:
        all_sys = ['']



    # List of variables we want to hadd
    var_list = [
    'closestJetDr',
    'lepPt',
    'lepEta',
    'nJets',
    'nTrkBtagJets',
    'mwt',
    'MET',
    'MET_phi',
    'closestJetPt',
    'largeJetPt',
    'largeJetM',
    # 'largeJetPtMtt',
    'largeJetEta',
    'largeJetPhi',
    'mtlep_boo',
    'mtlep_res',
    'mthad_res',
    'mwhad_res',
    'chi2',
    'largeJet_tau32_wta',
    'largeJet_tau21_wta',
    'yields',
    'mtt'
    ]

    print sysVar_list

    for p in process_list:
        tmp_sample = parse_json("filenames", campaign, p, var_list)
        extract_variables(tmp_sample, all_sys, PFrac, outpath)
        create_limit_inputs(tmp_sample, sysVar_list, PFrac, outpath)



# when calling this script
if __name__ == "__main__":
    main()



