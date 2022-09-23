 #!/usr/bin/env python

import os,sys
import ROOT
import argparse
from datetime import datetime
from systematics import *


today = datetime.date(datetime.now())



class sys_group:
    '''
    class defining systematics group objects
    grops consists of the systematics coming from the same source. Ex b-tagging
    '''
    def __init__ (self, group_name, name, title, symmetrization, category, sample_list, smoothing=False, correlation=False, regions="be1,be2,be3,re1,re2,re3,bmu1,bmu2,bmu3,rmu1,rmu2,rmu3"):
        self.group_name = group_name
        self.name = name
        self.title = title
        self.symmetrization = symmetrization
        self.category = category
        self.sample_list = sample_list
        self.regions = regions
        self.smoothing = smoothing
        self.correlation = correlation


def writeSysBlock(sys_group):
    '''
    Writes the systematics bocks for TRexFitter config
    retun:
    returns the systematic block in the form of string
    '''

    name_str = ''
    title_str = ''
    sys_cat = ''
    sample_list = ''
    for i in range(len(sys_group.name)):
        name_str += "\"{0}\";".format(sys_group.name[i])
        title_str += "\"{0}\";".format(sys_group.title[i])
    sys_cat += "\"{0}\"".format(sys_group.category)

    if all(x not in sys_group.group_name for x in ["tt_pdf", "MET_res"]):
        HistoNameSufUp_str = name_str.replace('";', '__1up";')
        HistoNameSufDown_str = name_str.replace('";', '__1down";')
    else:
        HistoNameSufUp_str = name_str
    sample_list = sys_group.sample_list
    regions = sys_group.regions


    block =  '''
Systematic: %s
  Title: %s
  Type: HISTO
  Samples: %s
  Regions: %s'''%(name_str, title_str, sample_list, regions)

    if sys_group.symmetrization == "TWOSIDED":
        block += '\n  HistoNameSufUp: %s'%HistoNameSufUp_str
        block += '\n  HistoNameSufDown: %s'%HistoNameSufDown_str
        block += '\n  Symmetrisation: %s'%sys_group.symmetrization
    elif sys_group.symmetrization == "ONESIDED":
        block += '\n  HistoNameSufUp: %s'%HistoNameSufUp_str
        block += '\n  Symmetrisation: %s'%sys_group.symmetrization
    elif sys_group.symmetrization == "NONE":
        block += '\n  HistoNameSufUp: %s'%HistoNameSufUp_str
        block += '\n  HistoNameSufDown: %s'%HistoNameSufDown_str
    block += "\n  Category: %s"%sys_cat
    if sys_group.smoothing:
             block += '\n  Smoothing: 40'
    if sys_group.correlation:
             block += '\n  Decorrelate:  REGION'
    print("\033[32;1m Adding %s systematics for samples = [%s] in the [%s] regions \033[0m"%(sys_group.group_name,sample_list,regions))

    return block

# make list of systematics names, hist_up and hist_down
def makeSysList(filename,channel, JESconfig='category', getFromFile=False):
    '''
    getFromFile: True   --> The systematic names will be read from the given root file
    getFromFile: Flase  --> The systematics names will be taken from the map
    
    return:
    returns a map of systematic group objects
    '''

    if JESconfig == 'global':
        JES_sysMap = JES_sysMap_global
        JMS_sysMap = JMS_sysMap_global
        JMR_sysMap = JMR_sysMap_global
    elif JESconfig == 'category':
        JES_sysMap = JES_sysMap_category
        JMS_sysMap = JMS_sysMap_category
        JMR_sysMap = JMR_sysMap_category
    else:
        print ("ERROR::Invalid JES configuration")

    sysName = []
    btag_sys_list = []
    toptag_sys_list = []
    JES_sys_list = []; JES_sys_model_list = []
    JMR_sys_list = []
    JER_sys_list = []
    JMS_sys_list = []
    MET_scale_sys_list = []
    MET_res_syst_list = []
    EG_syst_list = []
    MUON_syst_list = []

    sysblockMap = {}

    if getFromFile:
        infile=ROOT.TFile(filename,"READ") 

        for key in infile.GetListOfKeys():
            h= key.ReadObj()
            hname=ROOT.TString(h.GetName())
            if hname.Contains("SpuriousZprimeSignal") or hname.Contains("FitError"):
                continue
            if (hname.Contains(channel) and ( hname.EndsWith("__1up") or hname.EndsWith("__1down")) ):
                sysname=hname.Data().split(channel+"_mtt",1)[1]
                if (hname.Contains("__1up")):
                    sysname=sysname.split("__1up",1)[0]
                elif (hname.Contains("__1down")):
                    sysname=sysname.split("__1down",1)[0]

                if (not sysname in sysName):
                    sysName.append(sysname)
                    if "btag" in sysname:
                        btag_sys_list.append(sysname)
                    if "toptag" in sysname:
                        toptag_sys_list.append(sysname)
                    
                    if "JET_MassRes" in sysname:
                        JMR_sys_list.append(sysname)
                    elif "JER" in sysname:
                        JER_sys_list.append(sysname)
                    elif "JET_CombMass" in sysname:
                        JMS_sys_list.append(sysname)
                    elif "JET_" in sysname:
                        JES_sys_list.append(sysname)

                    print ("Got systematic: "+sysname)
    else:
        btag_sys_list = [x for x in btag_sysMap]
        toptag_sys_list = [x for x in toptag_sysMap]
        JES_sys_list = [x for x in JES_sysMap]
        JMR_sys_list = [x for x in JMR_sysMap]
        JER_sys_list = [x for x in JER_sysMap]
        JMS_sys_list = [x for x in JMS_sysMap]
        #JES_sys_model_list = [x for x in JES_sysMap_model]
        MET_scale_sys_list = [x for x in MET_scale_sysMap]
        MET_res_syst_list = [x for x in MET_res_sysMap]
        EG_sys_list = [x for x in EG_sysMap]
        MUON_sys_list = [x for x in MUON_sysMap]
        ttgen_sys_list = [x for x in ttgen_sysMap]
        ttmuF_sys_list = [x for x in ttmuF_sysMap]
        ttPDF_sys_list = [x for x in ttPDF_sysMap]
        ttNNLO_sys_list = [x for x in ttNNLO_sysMap]

    regions = "be1,be2,be3,re1,re2,re3,bmu1,bmu2,bmu3,rmu1,rmu2,rmu3"
    # regions = "b1,b2,b3,r1,r2,r3"
    # regions = "be1b,be2b,bmu1b,bmu2b,re1b,re2b,rmu1b,rmu2b"
    btag_sys = sys_group("btag_sys", btag_sys_list, [btag_sysMap[x] for x in btag_sys_list], "TWOSIDED", "b-tag", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    toptag_sys = sys_group("toptag_sys", toptag_sys_list, [toptag_sysMap[x] for x in toptag_sys_list], "TWOSIDED", "top-tag", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    JES_sys = sys_group("JES_sys", JES_sys_list, [JES_sysMap[x] for x in JES_sys_list], "TWOSIDED", "JES", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    #JES_modelling_sys = sys_group("JES_modelling_sys", JES_sys_model_list, [JES_sysMap_model[x] for x in JES_sys_model_list], "ONESIDED", False, regions=regions)
    JMR_sys = sys_group("JMR_sys", JMR_sys_list, [JMR_sysMap[x] for x in JMR_sys_list], "TWOSIDED", "JMR", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    JER_sys = sys_group("JER_sys", JER_sys_list, [JER_sysMap[x] for x in JER_sys_list], "TWOSIDED", "JER", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    JMS_sys = sys_group("JMS_sys", JMS_sys_list, [JMS_sysMap[x] for x in JMS_sys_list], "TWOSIDED", "JMS", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    MET_scale_sys = sys_group("MET_scale_sys", MET_scale_sys_list, [MET_scale_sysMap[x] for x in MET_scale_sys_list], "TWOSIDED", "MET-scale", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    MET_res_sys = sys_group("MET_res_sys", MET_res_syst_list, [MET_res_sysMap[x] for x in MET_res_syst_list], "ONESIDED", "MET-res", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    EG_sys = sys_group("EG_sys", EG_sys_list, [EG_sysMap[x] for x in EG_sys_list], "TWOSIDED", "EG", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)
    MUON_sys = sys_group("MUON_sys", MUON_sys_list, [MUON_sysMap[x] for x in MUON_sys_list], "TWOSIDED", "MUON", "Signal,tt,singletop,diboson,wjets,zjets", True, False, regions=regions)

    tt_gen_sys = sys_group("tt_gen_sys", ttgen_sys_list, [ttgen_sysMap[x] for x in ttgen_sys_list], "TWOSIDED", "tt_gen", "tt", True, True, regions=regions)
    tt_muF_sys = sys_group("tt_muF_sys", ttmuF_sys_list, [ttmuF_sysMap[x] for x in ttmuF_sys_list], "TWOSIDED", "tt_muF", "tt", True, True, regions=regions) #regions='be1,be2,be3,bmu1,bmu2,bmu3'
    tt_pdf_sys = sys_group("tt_pdf_sys", ttPDF_sys_list, [ttPDF_sysMap[x] for x in ttPDF_sys_list], "ONESIDED", "tt_pdf", "tt", True, False, regions=regions) #regions='re1,re2,re3,rmu1,rmu2,rmu3'
    tt_NNLO_sys = sys_group("tt_NNLO_sys", ttNNLO_sys_list, [ttNNLO_sysMap[x] for x in ttNNLO_sys_list], "TWOSIDED", "tt_NNLO", "tt", True, False, regions=regions)

    sys_groups = [btag_sys, toptag_sys, JES_sys, JMR_sys, JER_sys, JMS_sys, MET_scale_sys, MET_res_sys, EG_sys, MUON_sys, tt_gen_sys, tt_muF_sys, tt_pdf_sys, tt_NNLO_sys]

    for s in sys_groups:
        sysblockMap["%s"%s.group_name] = s

    return sysblockMap




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--indir",    type=str,  default="/eos/atlas/atlascerngroupdisk/phys-exotics/hqt/ttRes_semilep/TNA_outputs/histOutput_21.2.180_syst/fullrun2_aug2022/combined/limit_inputs",
                        help="The path to the input histogram files to be used")
    parser.add_argument("--outdir",       type=str,  default="statResults_tt1lep_%s"%today,
                        help="The path to the configs directory")
    parser.add_argument("--configdir",       type=str,  default="./configs_%s"%today,
                        help="The path to the output directory")
    parser.add_argument("--JESconfig",       type=str,  default="category",
                        help="JES configurations to be used: 'global' or 'category'")
    parser.add_argument("--region",       type=str,  default="combined",
                        help="Region to use in the limit: combined, 1bSR, 2bSR")
    parser.add_argument("--doSigInj", dest="doSigInj", default=False, action='store_true',
                        help="use --doSigInj if you want to inject signal")
    parser.add_argument("--suff", type=str,  default="",
                        help="suffix added to the outdir and configdir")


    args = parser.parse_args()

    inputDir        = args.indir
    outputDir       = args.outdir+'_'+args.suff
    configDir       = args.configdir+'_'+args.suff
    JESconfig       = args.JESconfig
    region          = args.region
    doSigInj        = args.doSigInj
    suff            = args.suff
    sigInject       = int(doSigInj)


    print ("=====================================================================")
    print ("INPUTS to the SCRIPT: ")
    print ("=====================================================================")
    print ("inputDir             : ", inputDir)
    print ("outputDir            : ", outputDir)
    print ("configDir            : ", configDir)
    print ("JESconfig            : ", JESconfig)
    print ("regions              : ", region)
    print ("signal Injection     : ", doSigInj)
    print ("suffix               : ", suff)
    print ("=====================================================================")

    homedir = os.getcwd()

    if sigInject:
        temp = homedir+"/configs/tt1lep_"+region+"_siginjection.config"
    else:
        # config with 4 b-tag SRs
        # temp = homedir+"/scripts/tt1lep_config.tmp"
        # Config with 16 b-tag SRs
        # temp = homedir+"/scripts/tt1lep_config_wbtagSR.tmp"
        # Config with N+ N- SRs
        # temp = homedir+"/scripts/tt1lep_config_wbtagSR_lepcharge.tmp"
        #config for W+jets CR
        #temp = homedir+"/scripts/tt1lep_WjetsCR_config.tmp"
        # 0 b-tag CR
        # temp = homedir+"/scripts/tt1lep_config_0btagCR.tmp"

        # Config with 12 b-tag SRs
        temp = homedir+"/scripts/tt1lep_config_wbtagSR_1b2b.tmp"

        # combined electron and muon channel
        # temp = homedir+"/scripts/tt1lep_config_wbtagSR_1b2b_mergedlep.tmp"

        # combined category 1 and category 2
        # temp = homedir+"/scripts/tt1lep_config_wbtagSR_1b2b_mergedbtag.tmp"


    #config file path
    configPATH_statonly = "{0}/configs/{1}/statonly/".format(homedir,configDir)
    configPATH_MCstat = "{0}/configs/{1}/MCstat/".format(homedir,configDir)
    configPATH_allsys = "{0}/configs/{1}/allsys/".format(homedir,configDir)

    #output flile path
    outPATH_statonly = "{0}/run/{1}/statonly".format(homedir,outputDir)
    outPATH_MCstat = "{0}/run/{1}/MCstat".format(homedir,outputDir)
    outPATH_allsys = "{0}/run/{1}/allsys".format(homedir,outputDir)
    outPATH_fitblind = "{0}/run/{1}/fitblind".format(homedir,outputDir)
    outPATH_statonly_fitblind = "{0}/run/{1}/statonly_fitblind".format(homedir,outputDir)

    outPATH_bonlyFit = "{0}/run/{1}/bonlyFit".format(homedir,outputDir)
    outPATH_bonly_allsys = "{0}/run/{1}/bonlyFit/allsys".format(homedir,outputDir)
    outPATH_bonly_allsys_fitblind = "{0}/run/{1}/bonlyFit/allsys_fitblind".format(homedir,outputDir)

    comd = "mkdir -p "+outPATH_statonly
    os.system(comd)
    comd = "mkdir -p "+outPATH_MCstat
    os.system(comd)
    comd = "mkdir -p "+outPATH_allsys
    os.system(comd)
    comd = "mkdir -p "+outPATH_fitblind
    os.system(comd)
    comd = "mkdir -p "+outPATH_statonly_fitblind
    os.system(comd)

    comd = "mkdir -p "+outPATH_bonlyFit
    os.system(comd)
    comd = "mkdir -p "+outPATH_bonly_allsys
    os.system(comd)
    comd = "mkdir -p "+outPATH_bonly_allsys_fitblind
    os.system(comd)

    comd = "mkdir -p "+configPATH_statonly
    os.system(comd)
    comd = "mkdir -p "+configPATH_MCstat
    os.system(comd)
    comd = "mkdir -p "+configPATH_allsys
    os.system(comd)


    #sys blocks
    sysmaps = makeSysList(inputDir+"/zprime2000.root", "b1SR", JESconfig, False)
    JES_sys_block = writeSysBlock(sysmaps["JES_sys"])
    JER_sys_block = writeSysBlock(sysmaps["JER_sys"])
    JMR_sys_block = writeSysBlock(sysmaps["JMR_sys"])
    JMS_sys_block = writeSysBlock(sysmaps["JMS_sys"])
    MET_scale_sys_block = writeSysBlock(sysmaps["MET_scale_sys"])
    MET_res_sys_block = writeSysBlock(sysmaps["MET_res_sys"])
    btag_sys_block = writeSysBlock(sysmaps["btag_sys"])
    toptag_sys_block = writeSysBlock(sysmaps["toptag_sys"])
    EG_sys_block = writeSysBlock(sysmaps["EG_sys"])
    MUON_sys_block = writeSysBlock(sysmaps["MUON_sys"])
    ttgen_sys_block = writeSysBlock(sysmaps["tt_gen_sys"])
    # ttmuF_sys_block = writeSysBlock(sysmaps["tt_muF_sys"])
    ttpdf_sys_block = writeSysBlock(sysmaps["tt_pdf_sys"])
    ttNNLO_sys_block = writeSysBlock(sysmaps["tt_NNLO_sys"])

 

    # read config template
    theTemplate = open(temp, 'r')
    theTemplateString  = theTemplate.read()
    string = theTemplateString.replace("INPUTDIR",inputDir)
    string = string.replace("TODAY",str(today))

    string_statonly = string.replace("STATONLY", "TRUE")
    string_statonly = string_statonly.replace("OUTPUTDIR",outPATH_statonly)
    config_statonly = open(configPATH_statonly+"zprime_"+region+"_StatOnly.config",'w')
    config_statonly.writelines(string_statonly)
    config_statonly.close()

    #All systematics configuration
    string_allsys = string.replace("STATONLY", "FALSE")
    string_allsys = string_allsys.replace("% BTAG_SYS",btag_sys_block)
    string_allsys = string_allsys.replace("% TOPTAG_SYS",toptag_sys_block)
    string_allsys = string_allsys.replace("% JES_SYS",JES_sys_block)
    string_allsys = string_allsys.replace("% JER_SYS",JER_sys_block)
    string_allsys = string_allsys.replace("% JMR_SYS",JMR_sys_block)
    string_allsys = string_allsys.replace("% JMS_SYS",JMS_sys_block)
    # # #MET
    string_allsys = string_allsys.replace("% MET_SCALE",MET_scale_sys_block)
    string_allsys = string_allsys.replace("% MET_RES",MET_res_sys_block)
    string_allsys = string_allsys.replace(r"% EG_SYS",EG_sys_block)
    string_allsys = string_allsys.replace("% MUON_SYS",MUON_sys_block)
    #ttbar generator, pdf and NNLO correction
    string_allsys = string_allsys.replace("% TTGEN_SYS",ttgen_sys_block)
    # string_allsys = string_allsys.replace("% TTMUF_SYS",ttmuF_sys_block)
    string_allsys = string_allsys.replace("% TTPDF_SYS",ttpdf_sys_block)
    string_allsys = string_allsys.replace("% TTNNLO_SYS",ttNNLO_sys_block)

    string_bonly_allsys = string_allsys.replace("SPLUSB", "BONLY")
    string_bonly_allsys = string_bonly_allsys.replace("OUTPUTDIR",outPATH_bonly_allsys)
    config_bonly_allsys = open(configPATH_allsys+"zprime_"+region+"_BONLY_AllSys.config",'w')
    config_bonly_allsys.writelines(string_bonly_allsys)
    config_bonly_allsys.close()

    string_allsys = string_allsys.replace("OUTPUTDIR",outPATH_allsys)
    config_allsys = open(configPATH_allsys+"zprime_"+region+"_AllSys.config",'w')
    config_allsys.writelines(string_allsys)
    config_allsys.close()

    del string, string_statonly, string_allsys, string_bonly_allsys
    del config_statonly, config_allsys, config_bonly_allsys



# when calling this script
if __name__ == "__main__":
    main()

