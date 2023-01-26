 #!/usr/bin/env python

import os,sys
import ROOT
import argparse
from datetime import datetime
from systematics import *
from pathlib import Path
from collections import namedtuple
from dataclasses import dataclass

today = datetime.date(datetime.now()) 


@dataclass(frozen=False)
class Settings:
    mass_out_dir: Path
    limit_dir: Path
    histo_dir: Path
    channel: str
    signal_name: str
    signal_injection_name: str
    region_1l: str
    region_2l: str
    ops: str
    mass: int
    signal_injection_mass: int
    seed: int
    auto_injection_strength: float
    fit_mu_asimov: float
    use_dilep_names: bool
    unblind: bool
    statonly: bool
    bonly: bool
    dry_run: bool
    exclude_systematics: list
    


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
    # print("\033[32;1m Adding %s systematics for samples = [%s] in the [%s] regions \033[0m"%(sys_group.group_name,sample_list,regions))

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

    btag_sys = sys_group("btag_sys", btag_sys_list, btag_dilepNamesMap, [btag_sysMap[x] for x in btag_sys_list], "TWOSIDED", "b-tag", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    toptag_sys = sys_group("toptag_sys", toptag_sys_list, {}, [toptag_sysMap[x] for x in toptag_sys_list], "TWOSIDED", "top-tag", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    JES_sys = sys_group("JES_sys", JES_sys_list, JES_dilepNamesMap, [JES_sysMap[x] for x in JES_sys_list], "TWOSIDED", "JES", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    #JES_modelling_sys = sys_group("JES_modelling_sys", JES_sys_model_list, [JES_sysMap_model[x] for x in JES_sys_model_list], "ONESIDED", False, regions=regions, use_dilep_names=use_dilep_names)
    JMR_sys = sys_group("JMR_sys", JMR_sys_list, {}, [JMR_sysMap[x] for x in JMR_sys_list], "TWOSIDED", "JMR", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    JER_sys = sys_group("JER_sys", JER_sys_list, JER_dilepNamesMap, [JER_sysMap[x] for x in JER_sys_list], "TWOSIDED", "JER", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    JMS_sys = sys_group("JMS_sys", JMS_sys_list, {},  [JMS_sysMap[x] for x in JMS_sys_list], "TWOSIDED", "JMS", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    MET_scale_sys = sys_group("MET_scale_sys", MET_scale_sys_list, MET_scale_dilepNamesMap, [MET_scale_sysMap[x] for x in MET_scale_sys_list], "TWOSIDED", "MET-scale", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    MET_res_sys = sys_group("MET_res_sys", MET_res_syst_list, MET_res_dilepNamesMap, [MET_res_sysMap[x] for x in MET_res_syst_list], "ONESIDED", "MET-res", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    EG_sys = sys_group("EG_sys", EG_sys_list, EG_dilepNamesMap, [EG_sysMap[x] for x in EG_sys_list], "TWOSIDED", "EG", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)
    MUON_sys = sys_group("MUON_sys", MUON_sys_list, MUON_dilepNamesMap, [MUON_sysMap[x] for x in MUON_sys_list], "TWOSIDED", "MUON", "Zprime*,KKg*,Grav*,tt,singletop,diboson,wjets,zjets", True, False, regions=regions, use_dilep_names=use_dilep_names)

    tt_gen_sys = sys_group("tt_gen_sys", ttgen_sys_list, {}, [ttgen_sysMap[x] for x in ttgen_sys_list], "TWOSIDED", "tt_gen", "tt", True, True, regions=regions, use_dilep_names=use_dilep_names)
    tt_muF_sys = sys_group("tt_muF_sys", ttmuF_sys_list, {}, [ttmuF_sysMap[x] for x in ttmuF_sys_list], "TWOSIDED", "tt_muF", "tt", True, True, regions=regions, use_dilep_names=use_dilep_names) #regions='be1,be2,be3,bmu1,bmu2,bmu3'
    tt_pdf_sys = sys_group("tt_pdf_sys", ttPDF_sys_list, {}, [ttPDF_sysMap[x] for x in ttPDF_sys_list], "ONESIDED", "tt_pdf", "tt", True, False, regions=regions, use_dilep_names=use_dilep_names) #regions='re1,re2,re3,rmu1,rmu2,rmu3'
    tt_NNLO_sys = sys_group("tt_NNLO_sys", ttNNLO_sys_list, {}, [ttNNLO_sysMap[x] for x in ttNNLO_sys_list], "TWOSIDED", "tt_NNLO", "tt", True, False, regions=regions, use_dilep_names=use_dilep_names)

    sys_groups = [btag_sys, toptag_sys, JES_sys, JMR_sys, JER_sys, JMS_sys, MET_scale_sys, MET_res_sys, EG_sys, MUON_sys, tt_gen_sys, tt_muF_sys, tt_pdf_sys, tt_NNLO_sys]

    return {s.group_name: s for s in sys_groups}


def add_common_settings_to_config_string(config_string: str, in_dir: Path, settings: Settings):
    config_string = config_string.replace("INPUTDIR", str(in_dir))
    config_string = config_string.replace("HISTODIR", str(settings.histo_dir))

    if settings.unblind:
        config_string = config_string.replace("BLIND", "FALSE")
    else:
        config_string = config_string.replace("BLIND", "TRUE")
    if settings.signal_injection_mass is not None:
        config_string = config_string.replace("INJMASS", str(settings.signal_injection_mass))
        config_string = config_string.replace("INJNAME", str(settings.signal_injection_name))
    if settings.auto_injection_strength is not None:
        config_string = config_string.replace("AUTOINJSTRENGTH", str(settings.auto_injection_strength))
        config_string = config_string.replace("AUTOINJ", "TRUE")
    else:
        config_string = config_string.replace("AUTOINJSTRENGTH", "0.0")
        config_string = config_string.replace("AUTOINJ", "FALSE")

    if settings.statonly:
        config_string = config_string.replace("STATONLY", "TRUE")
    else:
        config_string = config_string.replace("STATONLY", "FALSE")

    if settings.bonly:
        config_string = config_string.replace("SPLUSB", "BONLY")

    config_string = config_string.replace("OUTPUTDIR", str(settings.mass_out_dir))
    config_string = config_string.replace("SIGNALNAME", settings.signal_name)
    config_string = config_string.replace("SIGNALMASS", str(settings.mass))
    config_string = config_string.replace("FIT_POIASIMOV", str(settings.fit_mu_asimov))
    config_string = config_string.replace("SEED", str(settings.seed))

    return config_string

def add_systematics_to_1l_config_string(config_string: str, settings: Settings):
    #sys blocks
    sysmaps = makeSysList(settings.region_1l, use_dilep_names=settings.use_dilep_names)
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

    config_string = config_string.replace("% BTAG_SYS",btag_sys_block)
    config_string = config_string.replace("% TOPTAG_SYS",toptag_sys_block)
    config_string = config_string.replace("% JES_SYS",JES_sys_block)
    config_string = config_string.replace("% JER_SYS",JER_sys_block)
    config_string = config_string.replace("% JMR_SYS",JMR_sys_block)
    config_string = config_string.replace("% JMS_SYS",JMS_sys_block)
    #MET
    config_string = config_string.replace("% MET_SCALE",MET_scale_sys_block)
    config_string = config_string.replace("% MET_RES",MET_res_sys_block)
    config_string = config_string.replace(r"% EG_SYS",EG_sys_block)
    config_string = config_string.replace("% MUON_SYS",MUON_sys_block)
    #ttbar generator, pdf and NNLO correction
    config_string = config_string.replace("% TTGEN_SYS",ttgen_sys_block)
    # string_allsys = string_allsys.replace("% TTMUF_SYS",ttmuF_sys_block)
    config_string = config_string.replace("% TTPDF_SYS",ttpdf_sys_block)
    config_string = config_string.replace("% TTNNLO_SYS",ttNNLO_sys_block)

    return config_string

def get_common_opts(settings: Settings, regions: str):
    opts = []
    if settings.exclude_systematics:
        opts.append(f'Exclude={",".join(settings.exclude_systematics)}')
    opts.append(f'Regions={regions}')
    return opts

def make_1l_config(settings: Settings):
    """Make the config for the 1l channel"""

    # get path to parent directory of this script
    root_path = Path(os.path.realpath(__file__)).parent.parent
    config_dir = root_path / 'configs' / 'ttres1l'

    if settings.signal_injection_mass is not None:
        template_path = config_dir / "tt1lep_config_wbtagSR_1b2b_signal_injection.tmp"
    else:
        template_path = config_dir / "tt1lep_config_wbtagSR_1b2b.tmp"
 
    # set histogram path
    template_name = template_path.stem
    if settings.signal_injection_mass is not None:
        if settings.signal_injection_name == 'grav':
            signal_injection_name = 'Grav'
        elif settings.signal_injection_name == 'gluon':
            signal_injection_name = 'KKg'
        elif settings.signal_injection_name == 'zprime':
            signal_injection_name = 'ZprimeTC2'
        else:
            raise ValueError(f"Unknown signal injection name {settings.signal_injection_name}")
        settings.histo_dir = settings.histo_dir / 'ttres1l' / template_name / f'{signal_injection_name}_{settings.signal_injection_mass}_mu1.0'
    else:
        settings.histo_dir = settings.histo_dir / 'ttres1l' / template_name
        settings.histo_dir.mkdir(parents=True, exist_ok=True)

    # read config template
    with template_path.open('r') as f:
        config_string = f.read()

    #regions
    if settings.region_1l == 'combined':
        regions = "be1,be2,be3,re1,re2,re3,bmu1,bmu2,bmu3,rmu1,rmu2,rmu3"
    elif settings.region_1l == 'boosted':
        regions = "be1,be2,be3,bmu1,bmu2,bmu3"
    elif settings.region_1l == 'resolved':
        regions = "re1,re2,re3,rmu1,rmu2,rmu3"
    settings.region_1l = regions

    if not settings.statonly:
        config_string = add_systematics_to_1l_config_string(config_string, settings)

    in_dir = Path(os.environ['DATA_DIR_1L'])
    config_string = add_common_settings_to_config_string(config_string, in_dir, settings)

    # make command-line options for trexfitter
    opts = get_common_opts(settings, regions=regions)
    if settings.signal_name != 'all':
        opts.append(f'Signal={settings.signal_name}_{settings.mass}')
    opts = ':'.join(opts)

    return config_string, opts


def make_2l_config(settings: Settings):
    """Make the config for the 2l channel"""

    # get path to parent directory of this script
    root_path = Path(os.path.realpath(__file__)).parent.parent
    config_dir = root_path / 'configs' / 'ttres2l'

    if settings.signal_injection_mass is not None:
        raise NotImplementedError("Signal injection not implemented for 2l")
    else:
        template_path = config_dir / "ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll.tmp"

    # set input paths
    template_name = template_path.stem
    settings.histo_dir = settings.histo_dir / 'ttres2l' / template_name
    settings.histo_dir.mkdir(parents=True, exist_ok=True)
    
    # read config template
    with template_path.open('r') as f:
        config_string = f.read()

    # regions
    if settings.region_2l == 'mllbb':
        regions = "mllbb"
    elif settings.region_2l == 'deltaphi':
        regions = "DeltaPhi"
    elif settings.region_2l == 'mllbb_deltaphi':
        regions = "mllbb_DeltaPhi000to050,mllbb_DeltaPhi050to080,mllbb_DeltaPhi080to090,mllbb_DeltaPhi090to095,mllbb_DeltaPhi095to100"

    # common settings
    in_dir = Path(os.environ['DATA_DIR_2L'])
    config_string = add_common_settings_to_config_string(config_string, in_dir, settings)

    # make command-line options for trexfitter
    opts = get_common_opts(settings, regions=regions)
    if settings.signal_name != 'all':
        if settings.signal_name == 'ZprimeTC2':
            opts.append(f'Signal={settings.signal_name}_{settings.mass}')
        elif settings.signal_name == 'Grav':
            opts.append(f'Signal={settings.signal_name}{settings.mass}')
        elif settings.signal_name == 'KKg':
            opts.append(f'Signal={settings.signal_name}MG{settings.mass}')
    opts = ':'.join(opts)

    return config_string, opts

def make_combined_config(settings: Settings, config_1l: str, config_2l: str):
    string = string.replace("SINGLELEPCONFIG", str(config_1l)).replace("DILEPCONFIG", str(config_2l))
    opts = ''
    return string, opts
