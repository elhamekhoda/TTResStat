 #!/usr/bin/env python

import os,sys
import ROOT
import argparse
from datetime import datetime
from systematics import *
from pathlib import Path

today = datetime.date(datetime.now())



class sys_group:
    '''
    class defining systematics group objects
    grops consists of the systematics coming from the same source. Ex b-tagging
    '''
    def __init__ (self, group_name, name, dilep_names_dict, title, symmetrization, category, sample_list, smoothing=False, correlation=False, regions="be1,be2,be3,re1,re2,re3,bmu1,bmu2,bmu3,rmu1,rmu2,rmu3", use_dilep_names=False):
        self.group_name = group_name
        self.name = name
        if use_dilep_names:
            self.dilep_name = [dilep_names_dict[n] if (n in dilep_names_dict) else n for n in name]
        else:
            self.dilep_name = name
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
    dilep_name_str = ''
    title_str = ''
    sys_cat = ''
    sample_list = ''
    for i in range(len(sys_group.name)):
        name_str += "\"{0}\";".format(sys_group.name[i])
        dilep_name_str += "\"{0}\";".format(sys_group.dilep_name[i])
        title_str += "\"{0}\";".format(sys_group.title[i])
    sys_cat += "\"{0}\"".format(sys_group.category)

    if all(x not in sys_group.group_name for x in ["tt_pdf", "MET_res"]):
        HistoNameSufUp_str = name_str.replace('";', '__1up";')
        HistoNameSufDown_str = name_str.replace('";', '__1down";')
    else:
        HistoNameSufUp_str = name_str
    sample_list = sys_group.sample_list
    regions = sys_group.regions


    if sys_group.dilep_name:
        name_str = sys_group

    block =  '''
Systematic: %s
  Title: %s
  Type: HISTO
  Samples: %s
  Regions: %s'''%(dilep_name_str, title_str, sample_list, regions)

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
def makeSysList(regions, use_dilep_names=False):
    '''
    Makes the list of systematic groups.

    return:
    returns a map of systematic group objects
    '''

    JES_sysMap = JES_sysMap_category
    JMS_sysMap = JMS_sysMap_category
    JMR_sysMap = JMR_sysMap_category
    JES_dilepNamesMap = JES_dilepNamesMap_category

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

    btag_sys = sys_group("btag_sys", btag_sys_list, btag_dilepNamesMap, [btag_sysMap[x] for x in btag_sys_list], "TWOSIDED", "b-tag", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    toptag_sys = sys_group("toptag_sys", toptag_sys_list, {}, [toptag_sysMap[x] for x in toptag_sys_list], "TWOSIDED", "top-tag", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    JES_sys = sys_group("JES_sys", JES_sys_list, JES_dilepNamesMap, [JES_sysMap[x] for x in JES_sys_list], "TWOSIDED", "JES", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    #JES_modelling_sys = sys_group("JES_modelling_sys", JES_sys_model_list, [JES_sysMap_model[x] for x in JES_sys_model_list], "ONESIDED", False, regions=regions, use_dilep_names=use_dilep_names)
    JMR_sys = sys_group("JMR_sys", JMR_sys_list, {}, [JMR_sysMap[x] for x in JMR_sys_list], "TWOSIDED", "JMR", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    JER_sys = sys_group("JER_sys", JER_sys_list, JER_dilepNamesMap, [JER_sysMap[x] for x in JER_sys_list], "TWOSIDED", "JER", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    JMS_sys = sys_group("JMS_sys", JMS_sys_list, {},  [JMS_sysMap[x] for x in JMS_sys_list], "TWOSIDED", "JMS", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    MET_scale_sys = sys_group("MET_scale_sys", MET_scale_sys_list, MET_scale_dilepNamesMap, [MET_scale_sysMap[x] for x in MET_scale_sys_list], "TWOSIDED", "MET-scale", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    MET_res_sys = sys_group("MET_res_sys", MET_res_syst_list, MET_res_dilepNamesMap, [MET_res_sysMap[x] for x in MET_res_syst_list], "ONESIDED", "MET-res", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    EG_sys = sys_group("EG_sys", EG_sys_list, EG_dilepNamesMap, [EG_sysMap[x] for x in EG_sys_list], "TWOSIDED", "EG", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    MUON_sys = sys_group("MUON_sys", MUON_sys_list, MUON_dilepNamesMap, [MUON_sysMap[x] for x in MUON_sys_list], "TWOSIDED", "MUON", "SIGNALNAME_SIGNALMASS,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)

    tt_gen_sys = sys_group("tt_gen_sys", ttgen_sys_list, {}, [ttgen_sysMap[x] for x in ttgen_sys_list], "TWOSIDED", "tt_gen", "tt", True, True, regions=regions, use_dilep_names=use_dilep_names)
    tt_muF_sys = sys_group("tt_muF_sys", ttmuF_sys_list, {}, [ttmuF_sysMap[x] for x in ttmuF_sys_list], "TWOSIDED", "tt_muF", "tt", True, True, regions=regions, use_dilep_names=use_dilep_names) #regions='be1,be2,be3,bmu1,bmu2,bmu3'
    tt_pdf_sys = sys_group("tt_pdf_sys", ttPDF_sys_list, {}, [ttPDF_sysMap[x] for x in ttPDF_sys_list], "ONESIDED", "tt_pdf", "tt", True, False, regions=regions, use_dilep_names=use_dilep_names) #regions='re1,re2,re3,rmu1,rmu2,rmu3'
    tt_NNLO_sys = sys_group("tt_NNLO_sys", ttNNLO_sys_list, {}, [ttNNLO_sysMap[x] for x in ttNNLO_sys_list], "TWOSIDED", "tt_NNLO", "tt", True, False, regions=regions, use_dilep_names=use_dilep_names)

    sys_groups = [btag_sys, toptag_sys, JES_sys, JMR_sys, JER_sys, JMS_sys, MET_scale_sys, MET_res_sys, EG_sys, MUON_sys, tt_gen_sys, tt_muF_sys, tt_pdf_sys, tt_NNLO_sys]

    return {s.group_name: s for s in sys_groups}


def add_common_settings_to_config_string(string, in_dir, signal_injection_mass, signal_injection_name, unblind, auto_injection_strength, signal_name, signal_mass, statonly, bonly, out_dir):
    string = string.replace("INPUTDIR",in_dir)
    if unblind:
        string = string.replace("BLIND", "FALSE")
    else:
        string = string.replace("BLIND", "TRUE")
    if signal_injection_mass is not None:
        string = string.replace("INJMASS", str(signal_injection_mass))
        string = string.replace("INJNAME", str(signal_injection_name))
    if auto_injection_strength is not None:
        string = string.replace("AUTOINJSTRENGTH", str(auto_injection_strength))
        string = string.replace("AUTOINJ", "TRUE")
    else:
        string = string.replace("AUTOINJSTRENGTH", "0.0")
        string = string.replace("AUTOINJ", "FALSE")

    if statonly:
        string = string.replace("STATONLY", "TRUE")
    else:
        string = string.replace("STATONLY", "FALSE")

    if bonly:
        string = string.replace("SPLUSB", "BONLY")

    string = string.replace("OUTPUTDIR", str(out_dir))
    string = string.replace("SIGNALNAME", signal_name)
    string = string.replace("SIGNALMASS", str(signal_mass))

    return string

def add_systematics_to_1l_config_string(string, regions, use_dilep_names):
    #sys blocks
    sysmaps = makeSysList(regions, use_dilep_names=use_dilep_names)
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

    string = string.replace("% BTAG_SYS",btag_sys_block)
    string = string.replace("% TOPTAG_SYS",toptag_sys_block)
    string = string.replace("% JES_SYS",JES_sys_block)
    string = string.replace("% JER_SYS",JER_sys_block)
    string = string.replace("% JMR_SYS",JMR_sys_block)
    string = string.replace("% JMS_SYS",JMS_sys_block)
    #MET
    string = string.replace("% MET_SCALE",MET_scale_sys_block)
    string = string.replace("% MET_RES",MET_res_sys_block)
    string = string.replace(r"% EG_SYS",EG_sys_block)
    string = string.replace("% MUON_SYS",MUON_sys_block)
    #ttbar generator, pdf and NNLO correction
    string = string.replace("% TTGEN_SYS",ttgen_sys_block)
    # string_allsys = string_allsys.replace("% TTMUF_SYS",ttmuF_sys_block)
    string = string.replace("% TTPDF_SYS",ttpdf_sys_block)
    string = string.replace("% TTNNLO_SYS",ttNNLO_sys_block)

    return string

def make_1l_config(region, use_dilep_names, signal_injection_mass, signal_injection_name, unblind, auto_injection_strength, signal_name, signal_mass, statonly, bonly, mass_out_dir):
    """Make the config files for the limit setting
    region: the region to use in the limit: boosted, resolved, combined
    use_dilep_names: whether to use the dilepton naming convention for the input histograms
    signal_injection_mass: the mass of the signal to inject
    signal_injection_name: the name of the signal to inject
    unblind: whether to unblind
    auto_injection_strength: injection strength for TRExFitter auto signal injection
    signal_name: the name of the signal to use
    signal_mass: the mass of the signal to use
    statonly: whether to run  in stat-only mode
    bonly: whether to run the fit in background-only mode
    mass_out_dir: the run directory for this mass point
    """

    # get path to parent directory of this script
    root_path = Path(os.path.realpath(__file__)).parent.parent
    config_dir = root_path / 'configs' / 'ttres1l'

    if signal_injection_mass is not None:
        template_path = config_dir / "tt1lep_config_wbtagSR_1b2b_signal_injection.tmp"
    else:
        template_path = config_dir / "tt1lep_config_wbtagSR_1b2b.tmp"
 
    # read config template
    with template_path.open('r') as f:
        string = f.read()

    #regions
    if region == 'combined':
        regions = "be1,be2,be3,re1,re2,re3,bmu1,bmu2,bmu3,rmu1,rmu2,rmu3"
    elif region == 'boosted':
        regions = "be1,be2,be3,bmu1,bmu2,bmu3"
    elif region == 'resolved':
        regions = "re1,re2,re3,rmu1,rmu2,rmu3"

    region_text = ''
    for r in regions.split(','):
        region_config = config_dir / 'regions' / f'{r}.config'
        with region_config.open('r') as f:
            region_text += f.read() + '\n\n'
    string = string.replace('% REGIONS', region_text)

    if not statonly:
        string = add_systematics_to_1l_config_string(string, regions, use_dilep_names)

    in_dir = os.environ['DATA_DIR_1L']
    string = add_common_settings_to_config_string(string, in_dir, signal_injection_mass, signal_injection_name, unblind, auto_injection_strength, signal_name, signal_mass, statonly, bonly, mass_out_dir)

    return string


def make_2l_config(signal_injection_mass, signal_injection_name, unblind, auto_injection_strength, signal_name, signal_mass, statonly, bonly, mass_out_dir):
    # get path to parent directory of this script
    root_path = Path(os.path.realpath(__file__)).parent.parent
    config_dir = root_path / 'configs' / 'ttres2l'

    if signal_injection_mass is not None:
        raise NotImplementedError("Signal injection not implemented for 2l")
    else:
        template_path = config_dir / "ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll.tmp"

    # read config template
    with template_path.open('r') as f:
        string = f.read()

    in_dir = os.environ['DATA_DIR_2L']
    string = add_common_settings_to_config_string(string, in_dir, signal_injection_mass, signal_injection_name, unblind, auto_injection_strength, signal_name, signal_mass, statonly, bonly, mass_out_dir)

    return string

def make_combined_config():
    pass