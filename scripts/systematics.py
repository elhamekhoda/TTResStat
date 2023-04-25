#!/usr/bin/env python

from collections import OrderedDict

### ======= b-tagging SF uncertainties  ======= ###
btag_sysMap = OrderedDict()
btag_sysMap["btagbSF_0"] = "b-tag (E0)"
btag_sysMap["btagbSF_1"] = "b-tag (E1)"
btag_sysMap["btagbSF_2"] = "b-tag (E2)"
btag_sysMap["btagbSF_3"] = "b-tag (E3)"
btag_sysMap["btagbSF_4"] = "b-tag (E4)"
btag_sysMap["btagbSF_5"] = "b-tag (E5)"
btag_sysMap["btagbSF_6"] = "b-tag (E6)"
btag_sysMap["btagbSF_7"] = "b-tag (E7)"
btag_sysMap["btagbSF_8"] = "b-tag (E8)"
btag_sysMap["btagcSF_0"] = "c-mistag (E0)"
btag_sysMap["btagcSF_1"] = "c-mistag (E1)"
btag_sysMap["btagcSF_2"] = "c-mistag (E2)"
btag_sysMap["btagcSF_3"] = "c-mistag (E3)"
btag_sysMap["btageSF_0"] = "b-tag extrap."
btag_sysMap["btageSF_1"] = "c-mistag extrap."
btag_sysMap["btaglSF_0"] = "light-mistag (E0)"
btag_sysMap["btaglSF_1"] = "light-mistag (E1)"
btag_sysMap["btaglSF_2"] = "light-mistag (E2)"
btag_sysMap["btaglSF_3"] = "light-mistag (E3)"

btag_dilepNamesMap = OrderedDict()
btag_dilepNamesMap["btagbSF_0"] = 'btag_b_0'
btag_dilepNamesMap["btagbSF_1"] = 'btag_b_1'
btag_dilepNamesMap["btagbSF_2"] = 'btag_b_2'
btag_dilepNamesMap["btagbSF_3"] = 'btag_b_3'
btag_dilepNamesMap["btagbSF_4"] = 'btag_b_4'
btag_dilepNamesMap["btagbSF_5"] = 'btag_b_5'
btag_dilepNamesMap["btagbSF_6"] = 'btag_b_6'
btag_dilepNamesMap["btagbSF_7"] = 'btag_b_7'
btag_dilepNamesMap["btagbSF_8"] = 'btag_b_8'
btag_dilepNamesMap["btagcSF_0"] = 'btag_c_0'
btag_dilepNamesMap["btagcSF_1"] = 'btag_c_1'
btag_dilepNamesMap["btagcSF_2"] = 'btag_c_2'
btag_dilepNamesMap["btagcSF_3"] = 'btag_c_3'
btag_dilepNamesMap["btageSF_0"] = 'btag_extrap'
btag_dilepNamesMap["btageSF_1"] = 'btag_extrap_c'
btag_dilepNamesMap["btaglSF_0"] = 'btag_light_0'
btag_dilepNamesMap["btaglSF_1"] = 'btag_light_1'
btag_dilepNamesMap["btaglSF_2"] = 'btag_light_2'
btag_dilepNamesMap["btaglSF_3"] = 'btag_light_3'


btag_shortNames = OrderedDict()
btag_shortNames["btagbSF_0"] = "btagb0"
btag_shortNames["btagbSF_1"] = "btagb1"
btag_shortNames["btagbSF_2"] = "btagb2"
btag_shortNames["btagbSF_3"] = "btagb3"
btag_shortNames["btagbSF_4"] = "btagb4"
btag_shortNames["btagbSF_5"] = "btagb5"
btag_shortNames["btagbSF_6"] = "btagb6"
btag_shortNames["btagbSF_7"] = "btagb7"
btag_shortNames["btagbSF_8"] = "btagb8"
btag_shortNames["btagcSF_0"] = "btagc0"
btag_shortNames["btagcSF_1"] = "btagc1"
btag_shortNames["btagcSF_2"] = "btagc2"
btag_shortNames["btagcSF_3"] = "btagc3"
btag_shortNames["btageSF_0"] = "btage0"
btag_shortNames["btageSF_1"] = "btage1"
btag_shortNames["btaglSF_0"] = "btagl0"
btag_shortNames["btaglSF_1"] = "btagl1"
btag_shortNames["btaglSF_2"] = "btagl2"
btag_shortNames["btaglSF_3"] = "btagl3"


### ======= top-tagging SF uncertainties  ======= ###
toptag_sysMap = OrderedDict()
toptag_sysMap["toptagSF_0"] = r"top-tag (Dijet modelling)"
toptag_sysMap["toptagSF_1"] = r"top-tag (#gamma+jets modelling)"
toptag_sysMap["toptagSF_2"] = r"top-tag (t#bar{t} modelling, had.)"
toptag_sysMap["toptagSF_3"] = r"top-tag (t#bar{t} modelling, ME)"
toptag_sysMap["toptagSF_4"] = r"top-tag (t#bar{t} modelling, rad.)"
toptag_sysMap["toptagSF_5"] = r"top-tag (Dijet Stat.)"
toptag_sysMap["toptagSF_6"] = r"top-tag (#gamma+jets stat.)"
toptag_sysMap["toptagSF_7"] = r"top-tag (BGSF Prop.)"
toptag_sysMap["toptagSF_8"] = r"top-tag (SigSF BinVariation)"
toptag_sysMap["toptagSF_9"] = r"top-tag (high-p_{T} ext.  had.)"
toptag_sysMap["toptagSF_10"] = r"top-tag (SigSF prop.)"
toptag_sysMap["toptagSF_11"] = r"top-tag (SigSF stat.)"
# toptag_sysMap["toptagSF_12"] = r"top-tag (GlobalBackground)"
toptag_sysMap["toptagSF_13"] = r"top-tag (GlobalOther)"
toptag_sysMap["toptagSF_14"] = r"top-tag (GlobalSignal)"
toptag_sysMap["toptagSF_15"] = r"top-tag (bTag, B0)"
toptag_sysMap["toptagSF_16"] = r"top-tag (bTag, Light0)"
toptag_sysMap["toptagSF_17"] = r"top-tag (bTag, Light1)"

toptag_shortNames = OrderedDict()
toptag_shortNames["toptagSF_0"] = r"toptagSF0"
toptag_shortNames["toptagSF_1"] = r"toptagSF1"
toptag_shortNames["toptagSF_2"] = r"toptagSF2"
toptag_shortNames["toptagSF_3"] = r"toptagSF3"
toptag_shortNames["toptagSF_4"] = r"toptagSF4"
toptag_shortNames["toptagSF_5"] = r"toptagSF5"
toptag_shortNames["toptagSF_6"] = r"toptagSF6"
toptag_shortNames["toptagSF_7"] = r"toptagSF7"
toptag_shortNames["toptagSF_8"] = r"toptagSF8"
toptag_shortNames["toptagSF_9"] = r"toptagSF9"
toptag_shortNames["toptagSF_10"] = r"toptagSF10"
toptag_shortNames["toptagSF_11"] = r"toptagSF11"
toptag_shortNames["toptagSF_12"] = r"toptagSF12"
toptag_shortNames["toptagSF_13"] = r"toptagSF13"
toptag_shortNames["toptagSF_14"] = r"toptagSF14"
toptag_shortNames["toptagSF_15"] = r"toptagSF15"
toptag_shortNames["toptagSF_16"] = r"toptagSF16"
toptag_shortNames["toptagSF_17"] = r"toptagSF17"


### ========== JES Category reduction ============ ###
JES_sysMap_category = OrderedDict()
# Small-R jet
JES_sysMap_category['JET_EffectiveNP_Modelling1'] = r"AKT4 JES Modelling1"
JES_sysMap_category['JET_EffectiveNP_Modelling2'] = r"AKT4 JES Modelling2"
JES_sysMap_category['JET_EffectiveNP_Modelling3'] = r"AKT4 JES Modelling3"
JES_sysMap_category['JET_EffectiveNP_Modelling4'] = r"AKT4 JES Modelling4"
JES_sysMap_category['JET_EffectiveNP_Mixed1'] = r"AKT4 JES Mixed1"
JES_sysMap_category['JET_EffectiveNP_Mixed2'] = r"AKT4 JES Mixed2"
JES_sysMap_category['JET_EffectiveNP_Mixed3'] = r"AKT4 JES Mixed3"
JES_sysMap_category['JET_EffectiveNP_Detector1'] = r"AKT4 JES det1"
JES_sysMap_category['JET_EffectiveNP_Detector2'] = r"AKT4 JES det2"
JES_sysMap_category['JET_EffectiveNP_Statistical1'] = r"AKT4 JES stat1"
JES_sysMap_category['JET_EffectiveNP_Statistical2'] = r"AKT4 JES stat2"
JES_sysMap_category['JET_EffectiveNP_Statistical3'] = r"AKT4 JES stat3"
JES_sysMap_category['JET_EffectiveNP_Statistical4'] = r"AKT4 JES stat4"
JES_sysMap_category['JET_EffectiveNP_Statistical5'] = r"AKT4 JES stat5"
JES_sysMap_category['JET_EffectiveNP_Statistical6'] = r"AKT4 JES stat6"
JES_sysMap_category['JET_Pileup_OffsetMu'] = r"AKT4 JES pileup offset mu"
JES_sysMap_category['JET_Pileup_OffsetNPV'] = r"AKT4 JES pileup offset NPV"
JES_sysMap_category['JET_Pileup_PtTerm'] = r"AKT4 JES pileup pT term"
JES_sysMap_category['JET_Pileup_RhoTopology'] = r"AKT4 JES pileup RhoTopo"
JES_sysMap_category['JET_Flavor_Composition'] = r"AKT4 JES flav comp."
JES_sysMap_category['JET_Flavor_Response'] = r"AKT4 JES flav resp."
JES_sysMap_category['JET_BJES_Response'] = r"AKT4 b-JES"
JES_sysMap_category['JET_PunchThrough_MC16'] = r"AKT4 PunchThrough"
JES_sysMap_category['JET_SingleParticle_HighPt'] = r"AKT4 single part."
JES_sysMap_category['JET_EtaIntercalibration_Modelling'] = r"AKT4 #eta-int. Modeling"
JES_sysMap_category['JET_EtaIntercalibration_TotalStat'] = r"AKT4 JES #eta-int. TotalStat"
JES_sysMap_category['JET_EtaIntercalibration_NonClosure_highE'] = r"AKT4 JES #eta-int. highE"
JES_sysMap_category['JET_EtaIntercalibration_NonClosure_posEta'] = r"AKT4 JES #eta-int. posEta"
JES_sysMap_category['JET_EtaIntercalibration_NonClosure_negEta'] = r"AKT4 JES #eta-int. negEta"
JES_sysMap_category['JET_EtaIntercalibration_NonClosure_2018data'] = r"AKT4 JES #eta-int. 2018data"
# Large-R jet
JES_sysMap_category['JET_EffectiveNP_R10_Modelling1'] = r"AKT10 JES Modelling1"
JES_sysMap_category['JET_EffectiveNP_R10_Modelling2'] = r"AKT10 JES Modelling2"
JES_sysMap_category['JET_EffectiveNP_R10_Modelling3'] = r"AKT10 JES Modelling3"
JES_sysMap_category['JET_EffectiveNP_R10_Modelling4'] = r"AKT10 JES Modelling4"
JES_sysMap_category['JET_EffectiveNP_R10_Mixed1'] = r"AKT10 JES Mixed1"
JES_sysMap_category['JET_EffectiveNP_R10_Mixed2'] = r"AKT10 JES Mixed2"
JES_sysMap_category['JET_EffectiveNP_R10_Mixed3'] = r"AKT10 JES Mixed3"
JES_sysMap_category['JET_EffectiveNP_R10_Mixed4'] = r"AKT10 JES Mixed4"
JES_sysMap_category['JET_EffectiveNP_R10_Statistical1'] = r"AKT10 JES stat1"
JES_sysMap_category['JET_EffectiveNP_R10_Statistical2'] = r"AKT10 JES stat2"
JES_sysMap_category['JET_EffectiveNP_R10_Statistical3'] = r"AKT10 JES stat3"
JES_sysMap_category['JET_EffectiveNP_R10_Statistical4'] = r"AKT10 JES stat4"
JES_sysMap_category['JET_EffectiveNP_R10_Statistical5'] = r"AKT10 JES stat5"
JES_sysMap_category['JET_EffectiveNP_R10_Statistical6'] = r"AKT10 JES stat6"
JES_sysMap_category['JET_EffectiveNP_R10_Detector1'] = r"AKT10 JES det1"
JES_sysMap_category['JET_EffectiveNP_R10_Detector2'] = r"AKT10 JES det2"
JES_sysMap_category['JET_EtaIntercalibration_R10_TotalStat'] = r"AKT10 JES #eta-int stat"
JES_sysMap_category['JET_LargeR_TopologyUncertainty_top'] = r"AKT10 JES #eta-int top"
JES_sysMap_category['JET_LargeR_TopologyUncertainty_V'] = r"AKT10 JES #eta-int V"

JES_dilepNamesMap_category = OrderedDict()
JES_dilepNamesMap_category['JET_EffectiveNP_Modelling1'] = 'JES_EffectiveNP_Modelling1'
JES_dilepNamesMap_category['JET_EffectiveNP_Modelling2'] = 'JES_EffectiveNP_Modelling2'
JES_dilepNamesMap_category['JET_EffectiveNP_Modelling3'] = 'JES_EffectiveNP_Modelling3'
JES_dilepNamesMap_category['JET_EffectiveNP_Modelling4'] = 'JES_EffectiveNP_Modelling4'
JES_dilepNamesMap_category['JET_EffectiveNP_Mixed1'] = 'JES_EffectiveNP_Mixed1'
JES_dilepNamesMap_category['JET_EffectiveNP_Mixed2'] = 'JES_EffectiveNP_Mixed2'
JES_dilepNamesMap_category['JET_EffectiveNP_Mixed3'] = 'JES_EffectiveNP_Mixed3'
JES_dilepNamesMap_category['JET_EffectiveNP_Detector1'] = 'JES_EffectiveNP_Detector1'
JES_dilepNamesMap_category['JET_EffectiveNP_Detector2'] = 'JES_EffectiveNP_Detector2'
JES_dilepNamesMap_category['JET_EffectiveNP_Statistical1'] = 'JES_EffectiveNP_Statistical1'
JES_dilepNamesMap_category['JET_EffectiveNP_Statistical2'] = 'JES_EffectiveNP_Statistical2'
JES_dilepNamesMap_category['JET_EffectiveNP_Statistical3'] = 'JES_EffectiveNP_Statistical3'
JES_dilepNamesMap_category['JET_EffectiveNP_Statistical4'] = 'JES_EffectiveNP_Statistical4'
JES_dilepNamesMap_category['JET_EffectiveNP_Statistical5'] = 'JES_EffectiveNP_Statistical5'
JES_dilepNamesMap_category['JET_EffectiveNP_Statistical6'] = 'JES_EffectiveNP_Statistical6'
JES_dilepNamesMap_category['JET_Pileup_OffsetMu'] = 'JES_Pileup_OffsetMu'
JES_dilepNamesMap_category['JET_Pileup_OffsetNPV'] = 'JES_Pileup_OffsetNPV'
JES_dilepNamesMap_category['JET_Pileup_PtTerm'] = 'JES_Pileup_PtTerm'
JES_dilepNamesMap_category['JET_Pileup_RhoTopology'] = 'JES_Pileup_RhoTopology'
JES_dilepNamesMap_category['JET_Flavor_Composition'] = 'JES_Flavor_Comp'
JES_dilepNamesMap_category['JET_Flavor_Response'] = 'JES_Flavor_Resp'
JES_dilepNamesMap_category['JET_BJES_Response'] = 'JES_BJES_Resp'
JES_dilepNamesMap_category['JET_PunchThrough_MC16'] = 'JES_MC16'
JES_dilepNamesMap_category['JET_SingleParticle_HighPt'] = 'JES_SinglePart'
JES_dilepNamesMap_category['JET_EtaIntercalibration_Modelling'] = 'JES_EtaModelling'
JES_dilepNamesMap_category['JET_EtaIntercalibration_TotalStat'] = 'JES_EtatotStat'
JES_dilepNamesMap_category['JET_EtaIntercalibration_NonClosure_highE'] = 'JES_EtaNonClos_highE'
JES_dilepNamesMap_category['JET_EtaIntercalibration_NonClosure_posEta'] = 'JES_EtaNonClos_posEta'
JES_dilepNamesMap_category['JET_EtaIntercalibration_NonClosure_negEta'] = 'JES_EtaNonClos_negEta'
JES_dilepNamesMap_category['JET_EtaIntercalibration_NonClosure_2018data'] = 'JES_EtaNonClos_2018data'
# Large-R jet
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Modelling1'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Modelling2'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Modelling3'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Modelling4'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Mixed1'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Mixed2'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Mixed3'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Mixed4'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Statistical1'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Statistical2'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Statistical3'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Statistical4'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Statistical5'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Statistical6'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Detector1'] = ''
# JES_dilepNamesMap_category['JET_EffectiveNP_R10_Detector2'] = ''
# JES_dilepNamesMap_category['JET_EtaIntercalibration_R10_TotalStat'] = ''
# JES_dilepNamesMap_category['JET_LargeR_TopologyUncertainty_top'] = ''
# JES_dilepNamesMap_category['JET_LargeR_TopologyUncertainty_V'] = ''


JES_shortNames = OrderedDict()
# Small-R jet
JES_shortNames['JET_EffectiveNP_Modelling1'] = "akt4jesmodel1"
JES_shortNames['JET_EffectiveNP_Modelling2'] = "akt4jesmodel2"
JES_shortNames['JET_EffectiveNP_Modelling3'] = "akt4jesmodel3"
JES_shortNames['JET_EffectiveNP_Modelling4'] = "akt4jesmodel4"
JES_shortNames['JET_EffectiveNP_Mixed1'] = "akt4jesmixed1"
JES_shortNames['JET_EffectiveNP_Mixed2'] = "akt4jesmixed2"
JES_shortNames['JET_EffectiveNP_Mixed3'] = "akt4jesmixed3"
JES_shortNames['JET_EffectiveNP_Detector1'] = "akt4jesdet1"
JES_shortNames['JET_EffectiveNP_Detector2'] = "akt4jesdet2"
JES_shortNames['JET_EffectiveNP_Statistical1'] = "akt4jesstat1"
JES_shortNames['JET_EffectiveNP_Statistical2'] = "akt4jesstat2"
JES_shortNames['JET_EffectiveNP_Statistical3'] = "akt4jesstat3"
JES_shortNames['JET_EffectiveNP_Statistical4'] = "akt4jesstat4"
JES_shortNames['JET_EffectiveNP_Statistical5'] = "akt4jesstat5"
JES_shortNames['JET_EffectiveNP_Statistical6'] = "akt4jesstat6"
JES_shortNames['JET_Pileup_OffsetMu'] = "akt4jespileupmu"
JES_shortNames['JET_Pileup_OffsetNPV'] = "akt4jespileupNPV"
JES_shortNames['JET_Pileup_PtTerm'] = "akt4jespileuppt"
JES_shortNames['JET_Pileup_RhoTopology'] = "akt4jespileupRhoTopo"
JES_shortNames['JET_Flavor_Composition'] = "akt4jesflavcomp"
JES_shortNames['JET_Flavor_Response'] = "akt4jesflavresp"
JES_shortNames['JET_BJES_Response'] = "akt4jesbjes"
JES_shortNames['JET_PunchThrough_MC16'] = "akt4jespthrough"
JES_shortNames['JET_SingleParticle_HighPt'] = "akt4jessinglep"
JES_shortNames['JET_EtaIntercalibration_Modelling'] = "akt4jesetamod"
JES_shortNames['JET_EtaIntercalibration_TotalStat'] = "akt4jesetastat"
JES_shortNames['JET_EtaIntercalibration_NonClosure_highE'] = "akt4jeshighE"
JES_shortNames['JET_EtaIntercalibration_NonClosure_posEta'] = "akt4jesposEta"
JES_shortNames['JET_EtaIntercalibration_NonClosure_negEta'] = "akt4jesnegEta"
JES_shortNames['JET_EtaIntercalibration_NonClosure_2018data'] = "akt4jes2018data"
# Large-R jet
JES_shortNames['JET_EffectiveNP_R10_Modelling1'] = r"akt10model1"
JES_shortNames['JET_EffectiveNP_R10_Modelling2'] = r"akt10model2"
JES_shortNames['JET_EffectiveNP_R10_Modelling3'] = r"akt10model3"
JES_shortNames['JET_EffectiveNP_R10_Modelling4'] = r"akt10model4"
JES_shortNames['JET_EffectiveNP_R10_Mixed1'] = r"akt10mixed1"
JES_shortNames['JET_EffectiveNP_R10_Mixed2'] = r"akt10mixed2"
JES_shortNames['JET_EffectiveNP_R10_Mixed3'] = r"akt10mixed3"
JES_shortNames['JET_EffectiveNP_R10_Mixed4'] = r"akt10mixed4"
JES_shortNames['JET_EffectiveNP_R10_Statistical1'] = r"akt10stat1"
JES_shortNames['JET_EffectiveNP_R10_Statistical2'] = r"akt10stat2"
JES_shortNames['JET_EffectiveNP_R10_Statistical3'] = r"akt10stat3"
JES_shortNames['JET_EffectiveNP_R10_Statistical4'] = r"akt10stat4"
JES_shortNames['JET_EffectiveNP_R10_Statistical5'] = r"akt10stat5"
JES_shortNames['JET_EffectiveNP_R10_Statistical6'] = r"akt10stat6"
JES_shortNames['JET_EffectiveNP_R10_Detector1'] = r"akt10det1"
JES_shortNames['JET_EffectiveNP_R10_Detector2'] = r"akt10det2"
JES_shortNames['JET_EtaIntercalibration_R10_TotalStat'] = r"akt10etastat"
JES_shortNames['JET_LargeR_TopologyUncertainty_top'] = r"akt10etatop"
JES_shortNames['JET_LargeR_TopologyUncertainty_V'] = r"akt10etaV"


### ========== JER Category reduction ============ ###
JER_sysMap = OrderedDict()
# Small-R jet
JER_sysMap['JET_JER_EffectiveNP_1'] = r"AKT4 JER NP1"
JER_sysMap['JET_JER_EffectiveNP_2'] = r"AKT4 JER NP2"
JER_sysMap['JET_JER_EffectiveNP_3'] = r"AKT4 JER NP3"
JER_sysMap['JET_JER_EffectiveNP_4'] = r"AKT4 JER NP4"
JER_sysMap['JET_JER_EffectiveNP_5'] = r"AKT4 JER NP5"
JER_sysMap['JET_JER_EffectiveNP_6'] = r"AKT4 JER NP6"
JER_sysMap['JET_JER_EffectiveNP_7'] = r"AKT4 JER NP7"
JER_sysMap['JET_JER_EffectiveNP_8'] = r"AKT4 JER NP8"
JER_sysMap['JET_JER_EffectiveNP_9'] = r"AKT4 JER NP9"
JER_sysMap['JET_JER_EffectiveNP_10'] = r"AKT4 JER NP10"
JER_sysMap['JET_JER_EffectiveNP_11'] = r"AKT4 JER NP11"
JER_sysMap['JET_JER_EffectiveNP_12restTerm'] = r"AKT4 JER NP12"
# JER_sysMap['JET_JER_DataVsMC_MC16'] = r"AKT4 JER dataMC"
# Large-R jet
JER_sysMap['JET_JER_DataVsMC_R10_MC16'] = r"AKT10 JER DataVsMC"
JER_sysMap['JET_JER_dijet_R10_closure'] = r"AKT10 JER closure"
JER_sysMap['JET_JER_dijet_R10_selection'] = r"AKT10 JER evnt sel"
JER_sysMap['JET_JER_dijet_R10_jesEffNP1'] = r"AKT10 JER NP1"
JER_sysMap['JET_JER_dijet_R10_jesEffNP3'] = r"AKT10 JER NP3"
JER_sysMap['JET_JER_dijet_R10_jesEffNP4'] = r"AKT10 JER NP4"
JER_sysMap['JET_JER_dijet_R10_jesEtaIntMod'] = r"AKT10 JER #eta-int. Modeling"
JER_sysMap['JET_JER_dijet_R10_jesFlavComp'] = r"AKT10 JER flav comp."
JER_sysMap['JET_JER_dijet_R10_jesFlavResp'] = r"AKT10 JER flav resp."
JER_sysMap['JET_JER_dijet_R10_mcgenerator'] = r"AKT10 JER MC-gen"
JER_sysMap['JET_JER_dijet_R10_stat'] = r"AKT10 JER NP stat"
JER_sysMap['JET_JER_AllOthers'] = r"AKT10 JER Allother"


JER_dilepNamesMap = OrderedDict()
# Small-R jet
JER_dilepNamesMap['JET_JER_EffectiveNP_1'] = 'JER_EffectiveNP1'
JER_dilepNamesMap['JET_JER_EffectiveNP_2'] = 'JER_EffectiveNP2'
JER_dilepNamesMap['JET_JER_EffectiveNP_3'] = 'JER_EffectiveNP3'
JER_dilepNamesMap['JET_JER_EffectiveNP_4'] = 'JER_EffectiveNP4'
JER_dilepNamesMap['JET_JER_EffectiveNP_5'] = 'JER_EffectiveNP5'
JER_dilepNamesMap['JET_JER_EffectiveNP_6'] = 'JER_EffectiveNP6'
JER_dilepNamesMap['JET_JER_EffectiveNP_7'] = 'JER_EffectiveNP7'
JER_dilepNamesMap['JET_JER_EffectiveNP_8'] = 'JER_EffectiveNP8'
JER_dilepNamesMap['JET_JER_EffectiveNP_9'] = 'JER_EffectiveNP9'
JER_dilepNamesMap['JET_JER_EffectiveNP_10'] = 'JER_EffectiveNP10'
JER_dilepNamesMap['JET_JER_EffectiveNP_11'] = 'JER_EffectiveNP11'
JER_dilepNamesMap['JET_JER_EffectiveNP_12restTerm'] = 'JER_EffectiveNP_12restTerm'
JER_dilepNamesMap['JET_JER_DataVsMC_MC16'] = 'JER_DataVsMC_MC16'
# Large-R jet
# JER_dilepNamesMap['JET_JER_DataVsMC_R10_MC16'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_closure'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_selection'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_jesEffNP1'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_jesEffNP3'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_jesEffNP4'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_jesEtaIntMod'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_jesFlavComp'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_jesFlavResp'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_mcgenerator'] = ''
# JER_dilepNamesMap['JET_JER_dijet_R10_stat'] = ''
# JER_dilepNamesMap['JET_JER_AllOthers'] = ''

JER_shortNames = OrderedDict()
# Small-R jet
JER_shortNames['JET_JER_EffectiveNP_1'] = r"akt4jernp1"
JER_shortNames['JET_JER_EffectiveNP_2'] = r"akt4jernp2"
JER_shortNames['JET_JER_EffectiveNP_3'] = r"akt4jernp3"
JER_shortNames['JET_JER_EffectiveNP_4'] = r"akt4jernp4"
JER_shortNames['JET_JER_EffectiveNP_5'] = r"akt4jernp5"
JER_shortNames['JET_JER_EffectiveNP_6'] = r"akt4jernp6"
JER_shortNames['JET_JER_EffectiveNP_7'] = r"akt4jernp7"
JER_shortNames['JET_JER_EffectiveNP_8'] = r"akt4jernp8"
JER_shortNames['JET_JER_EffectiveNP_9'] = r"akt4jernp9"
JER_shortNames['JET_JER_EffectiveNP_10'] = r"akt4jernp10"
JER_shortNames['JET_JER_EffectiveNP_11'] = r"akt4jernp11"
JER_shortNames['JET_JER_EffectiveNP_12restTerm'] = r"akt4jernp12"
JER_shortNames['JET_JER_DataVsMC_MC16'] = r"akt4jermc16"
# Large-R jet
JER_shortNames['JET_JER_DataVsMC_R10_MC16'] = r"akt10DataVsMC"
JER_shortNames['JET_JER_dijet_R10_closure'] = r"akt10closure"
JER_shortNames['JET_JER_dijet_R10_selection'] = r"akt10evntsel"
JER_shortNames['JET_JER_dijet_R10_jesEffNP1'] = r"akt10np1"
JER_shortNames['JET_JER_dijet_R10_jesEffNP3'] = r"akt10np3"
JER_shortNames['JET_JER_dijet_R10_jesEffNP4'] = r"akt10np4"
JER_shortNames['JET_JER_dijet_R10_jesEtaIntMod'] = r"akt10etamodel"
JER_shortNames['JET_JER_dijet_R10_jesFlavComp'] = r"akt10flavcomp"
JER_shortNames['JET_JER_dijet_R10_jesFlavResp'] = r"akt10flavresp"
JER_shortNames['JET_JER_dijet_R10_mcgenerator'] = r"akt10MCgen"
JER_shortNames['JET_JER_dijet_R10_stat'] = r"akt10NPstat"
JER_shortNames['JET_JER_AllOthers'] = r"akt10Allother"


### ========== JMS Category reduction ============ ###
JMS_sysMap_category = OrderedDict()
JMS_sysMap_category['JET_JMS_Rtrk_Stat1'] = r"AKT10 JMS R_{trk} stat1"
JMS_sysMap_category['JET_JMS_Rtrk_Stat2'] = r"AKT10 JMS R_{trk} stat2"
JMS_sysMap_category['JET_JMS_Rtrk_Stat3'] = r"AKT10 JMS R_{trk} stat3"
JMS_sysMap_category['JET_JMS_Rtrk_Stat4'] = r"AKT10 JMS R_{trk} stat4"
JMS_sysMap_category['JET_JMS_Rtrk_Stat5'] = r"AKT10 JMS R_{trk} stat5"
JMS_sysMap_category['JET_JMS_Rtrk_Stat6'] = r"AKT10 JMS R_{trk} stat6"
JMS_sysMap_category['JET_JMS_Rtrk_Tracking'] = r"AKT10 JMS R_{trk} tracking"
JMS_sysMap_category['JET_JMS_Rtrk_Generator'] = r"AKT10 JMS R_{trk} gen."
JMS_sysMap_category['JET_JMS_Rtrk_Generator_InterpolationDifference'] = r"AKT10 JMS R_{trk} gen. int."
JMS_sysMap_category['JET_JMS_Rtrk_InterpolationDifference'] = r"AKT10 JMS R_{trk} int."
JMS_sysMap_category['JET_JMS_FF_LargerSample'] = r"AKT10 JMS FF_LargerSample"
JMS_sysMap_category['JET_JMS_FF_MatrixElement'] = r"AKT10 JMS FF ME"
JMS_sysMap_category['JET_JMS_FF_PartonShower'] = r"AKT10 JMS FF PS"
JMS_sysMap_category['JET_JMS_FF_Shape'] = r"AKT10 JMS FF shape"
JMS_sysMap_category['JET_JMS_FF_Stat'] = r"AKT10 JMS FF stat"
JMS_sysMap_category['JET_JMS_FF_InterpolationDifference'] = r"AKT10 JMS FF int."
JMS_sysMap_category['JET_JMS_FF_AllOthers'] = r"AKT10 JMS FF AllOthers"
JMS_sysMap_category['JET_JMS_Topology_QCD'] = r"AKT10 JMS topo QCD"

JMS_shortNames = OrderedDict()
JMS_shortNames['JET_JMS_Rtrk_Stat1'] = r"akt10jmsstat1"
JMS_shortNames['JET_JMS_Rtrk_Stat2'] = r"akt10jmsstat2"
JMS_shortNames['JET_JMS_Rtrk_Stat3'] = r"akt10jmsstat3"
JMS_shortNames['JET_JMS_Rtrk_Stat4'] = r"akt10jmsstat4"
JMS_shortNames['JET_JMS_Rtrk_Stat5'] = r"akt10jmsstat5"
JMS_shortNames['JET_JMS_Rtrk_Stat6'] = r"akt10jmsstat6"
JMS_shortNames['JET_JMS_Rtrk_Tracking'] = r"akt10jmstracking"
JMS_shortNames['JET_JMS_Rtrk_Generator'] = r"akt10jmsgen"
JMS_shortNames['JET_JMS_Rtrk_Generator_InterpolationDifference'] = r"akt10jmsgenint"
JMS_shortNames['JET_JMS_Rtrk_InterpolationDifference'] = r"akt10jmsint"
JMS_shortNames['JET_JMS_FF_LargerSample'] = r"akt10jmsFFLargerSample"
JMS_shortNames['JET_JMS_FF_MatrixElement'] = r"akt10jmsFFME"
JMS_shortNames['JET_JMS_FF_PartonShower'] = r"akt10jmsFFPS"
JMS_shortNames['JET_JMS_FF_Shape'] = r"akt10jmsFFshape"
JMS_shortNames['JET_JMS_FF_Stat'] = r"akt10jmsFFstat"
JMS_shortNames['JET_JMS_FF_InterpolationDifference'] = r"akt10jmsFFint"
JMS_shortNames['JET_JMS_FF_AllOthers'] = r"akt10jmsFFallOthers"
JMS_shortNames['JET_JMS_Topology_QCD'] = r"akt10jmstopoQCD"


### ========== JMR Category reduction ============ ###
JMR_sysMap_category = OrderedDict()
JMR_sysMap_category['COMB_MCData_JMR'] = r"JMR COMB MCData"
JMR_sysMap_category['COMB_MCME_JMR'] = r"JMR COMB MCME"
JMR_sysMap_category['COMB_MCPS_JMR'] = r"JMR COMB MCPS"
JMR_sysMap_category['COMB_MCRAD_JMR'] = r"JMR COMB MCRAD"
JMR_sysMap_category['COMB_MCSmallJET_JMR'] = r"JMR COMB MCSmall jet"
JMR_sysMap_category['COMB_MCLargeR_JMR'] = r"JMR COMB MCLargeR jet"
JMR_sysMap_category['COMB_Stat_JMR'] = r"JMR COMB Stat"
JMR_sysMap_category['COMB_SHAPE_JMR'] = r"JMR COMB shape"
JMR_sysMap_category['COMB_Smoothing_JMR'] = r"JMR COMB smoothing"
JMR_sysMap_category['COMB_Flat20Smoothed_JMR'] = r"JMR COMB Flat20smoothed"
JMR_sysMap_category['COMB_OutsideCalib_JMR'] = r"JMR COMB outsideCalib"

JMR_shortNames = OrderedDict()
JMR_shortNames['COMB_MCData_JMR'] = r"jmrMCData"
JMR_shortNames['COMB_MCME_JMR'] = r"jmrMCME"
JMR_shortNames['COMB_MCPS_JMR'] = r"jmrMCPS"
JMR_shortNames['COMB_MCRAD_JMR'] = r"jmrMCRAD"
JMR_shortNames['COMB_MCSmallJET_JMR'] = r"jmrMCSmalljet"
JMR_shortNames['COMB_MCLargeR_JMR'] = r"jmrMCLargeRjet"
JMR_shortNames['COMB_Stat_JMR'] = r"jmrStat"
JMR_shortNames['COMB_SHAPE_JMR'] = r"jmrshape"
JMR_shortNames['COMB_Smoothing_JMR'] = r"jmrsmoothing"
JMR_shortNames['COMB_Flat20Smoothed_JMR'] = r"jmrFlat20smoothed"
JMR_shortNames['COMB_OutsideCalib_JMR'] = r"jmroutsideCalib"


### ========== MET systematics ============ ###
MET_scale_sysMap = OrderedDict()
MET_scale_sysMap['MET_SoftTrk_Scale'] = r"E_{T}^{miss} soft track scale"

MET_scale_dilepNamesMap = OrderedDict()
MET_scale_dilepNamesMap['MET_SoftTrk_Scale'] = 'MET_SoftTrk_Scale'

MET_scale_shortNames = OrderedDict()
MET_scale_shortNames['MET_SoftTrk_Scale'] = "metscale"

MET_res_sysMap = OrderedDict()
MET_res_sysMap['MET_SoftTrk_ResoPara'] = r"E_{T}^{miss} soft track resolution (para.)"
MET_res_sysMap['MET_SoftTrk_ResoPerp'] = r"E_{T}^{miss} soft track resolution (perp.)"

MET_res_dilepNamesMap = OrderedDict()

MET_res_dilepNamesMap['MET_SoftTrk_ResoPara'] = 'MET_SoftTrk_ResoPara'
MET_res_dilepNamesMap['MET_SoftTrk_ResoPerp'] = 'MET_SoftTrk_ResoPerp'

MET_res_shortNames = OrderedDict()
MET_res_shortNames['MET_SoftTrk_ResoPara'] = "metresopara"
MET_res_shortNames['MET_SoftTrk_ResoPerp'] = "metresoperp"


### ========== EGamma systematics ============ ###
EG_sysMap = OrderedDict()
EG_sysMap['EG_RESOLUTION_ALL'] = r"EL res"
EG_sysMap['EG_SCALE_ALL'] = r"EL scale"
EG_sysMap['eChargeMisIDStatSF'] = r"EL ChargeMisIDStatSF"
EG_sysMap['eChargeMisIDSystSF'] = r"EL ChargeMisIDSystSF"
EG_sysMap['eChargeSF'] = r"EL ChargeSF"
EG_sysMap['eIDSF'] = r"EL IDSF"
EG_sysMap['eIsolSF'] = r"EL IsoSF"
EG_sysMap['eRecoSF'] = r"EL RecoSF"
EG_sysMap['eTrigSF'] = r"EL TrigSF"

EG_dilepNamesMap = OrderedDict()
EG_dilepNamesMap['EG_RESOLUTION_ALL'] = 'EG_RESOLUTION_ALL'
EG_dilepNamesMap['EG_SCALE_ALL'] = 'EG_SCALE_ALL'
# EG_dilepNamesMap['eChargeMisIDStatSF'] =
# EG_dilepNamesMap['eChargeMisIDSystSF'] = 
# EG_dilepNamesMap['eChargeSF'] = 
EG_dilepNamesMap['eIDSF'] = 'leptonSF_EL_SF_ID'
EG_dilepNamesMap['eIsolSF'] = 'leptonSF_EL_SF_Isol'
EG_dilepNamesMap['eRecoSF'] = 'leptonSF_EL_SF_Reco'
EG_dilepNamesMap['eTrigSF'] = 'leptonSF_EL_SF_Trigger'

EG_shortNames = OrderedDict()
EG_shortNames['EG_RESOLUTION_ALL'] = r"elres"
EG_shortNames['EG_SCALE_ALL'] = r"elscale"
EG_shortNames['eChargeMisIDStatSF'] = r"elChargeMisIDStatSF"
EG_shortNames['eChargeMisIDSystSF'] = r"elChargeMisIDSystSF"
EG_shortNames['eChargeSF'] = r"elChargeSF"
EG_shortNames['eIDSF'] = r"elIDSF"
EG_shortNames['eIsolSF'] = r"elIsoSF"
EG_shortNames['eRecoSF'] = r"elRecoSF"
EG_shortNames['eTrigSF'] = r"elTrigSF"


### ========== MUON systematics ============ ###
MUON_sysMap = OrderedDict()
MUON_sysMap['MUON_SAGITTA_RESBIAS'] = r"Muon sagitta resbias"
MUON_sysMap['MUON_SAGITTA_RHO'] = r"Muon sagitta rho"
MUON_sysMap['MUON_SCALE'] = r"Muon scale"
MUON_sysMap['MUON_ID'] = r"Muon ID"
MUON_sysMap['MUON_MS'] = r"Muon MS"
MUON_sysMap['muIDStatSF'] ="Muon IDStatSF"
MUON_sysMap['muIDSystSF'] = "Muon IDSystSF"
MUON_sysMap['muIsolStatSF'] = "Muon IsolStatSF"
MUON_sysMap['muIsolSystSF'] = "Muon IsolSystSF"
MUON_sysMap['muTrigStatSF'] = "Muon TrigStatSF"
MUON_sysMap['muTrigSystSF'] = "Muon TrigSystSF"

MUON_dilepNamesMap = OrderedDict()
MUON_dilepNamesMap['MUON_SAGITTA_RESBIAS'] = 'MUON_Sagitta'
# MUON_dilepNamesMap['MUON_SAGITTA_RHO'] =
MUON_dilepNamesMap['MUON_SCALE'] = 'MUON_Scale'
MUON_dilepNamesMap['MUON_ID'] = 'MUON_ID'
MUON_dilepNamesMap['MUON_MS'] = 'MUON_MS'
MUON_dilepNamesMap['muIDStatSF'] = 'leptonSF_MU_SF_ID_STAT'
MUON_dilepNamesMap['muIDSystSF'] = 'leptonSF_MU_SF_ID_SYST'
MUON_dilepNamesMap['muIsolStatSF'] = 'leptonSF_MU_SF_Isol_STAT'
MUON_dilepNamesMap['muIsolSystSF'] = 'leptonSF_MU_SF_Isol_SYST'
MUON_dilepNamesMap['muTrigStatSF'] = 'leptonSF_MU_SF_Trigger_STAT'
MUON_dilepNamesMap['muTrigSystSF'] = 'leptonSF_MU_SF_Trigger_SYST'

MUON_shortNames = OrderedDict()
MUON_shortNames['MUON_SAGITTA_RESBIAS'] = r"muonsagittaresbias"
MUON_shortNames['MUON_SAGITTA_RHO'] = r"muonsagittarho"
MUON_shortNames['MUON_SCALE'] = r"muonscale"
MUON_shortNames['MUON_ID'] = r"muonID"
MUON_shortNames['MUON_MS'] = r"muonMS"
MUON_shortNames['muIDStatSF'] ="muonIDStatSF"
MUON_shortNames['muIDSystSF'] = "muonIDSystSF"
MUON_shortNames['muIsolStatSF'] = "muonIsolStatSF"
MUON_shortNames['muIsolSystSF'] = "muonIsolSystSF"
MUON_shortNames['muTrigStatSF'] = "muonTrigStatSF"
MUON_shortNames['muTrigSystSF'] = "muonTrigSystSF"


### ========== ttbar Generator SF systematics ============ ###
ttgen_sysMap = OrderedDict()
ttgen_sysMap["tt_muR"] = r"t#bar{t} #mu_{R} Scale"
ttgen_sysMap["tt_muF"] = r"t#bar{t} #mu_{F} Scale"
ttgen_sysMap["tt_ISR"] = r"t#bar{t} ISR (#alpha_{S})"
ttgen_sysMap["tt_FSR"] = r"t#bar{t} FSR (#alpha_{S})"

ttmuF_sysMap = OrderedDict()
ttmuF_sysMap["tt_muF"] = r"t#bar{t} #mu_{F} Scale"


### ========== ttbar PDF systematics ============ ###
ttPDF_sysMap = OrderedDict()
for i in range(1,31):
    ttPDF_sysMap["tt_pdf_%s"%str(i)] = r"t#bar{t} PDF %s"%str(i)


### ========== ttbar NNLO RW systematics ============ ###
ttNNLO_sysMap = OrderedDict()
ttNNLO_sysMap["ttNNLOrec_toppt"] = r"t#bar{t} NNLO scale (p_{T} (t))"
ttNNLO_sysMap["ttNNLOrec_ttmass"] = r"t#bar{t} NNLO scale (m (t#bar{t}))"
# ttNNLO_sysMap["ttNNLOrec_ttpt"] = r"t#bar{t} NNLO scale (p_{T} (t#bar{t}))"


### ========== JVT, Pileup, Lumi ============ ###
sysMap = OrderedDict()
sysMap["jvtSF"] ="JVT"
sysMap["pileupSF"] ="pileup modelling"
# sysMap["lumi"] ="Luminosity"

sys_dilepNamesMap = OrderedDict()
sys_dilepNamesMap['jvtSF'] = 'jvt'
sys_dilepNamesMap['pileupSF'] = 'pileup'
sys_dilepNamesMap['lumi'] = 'Lumi'

# combine all _dilepNamesMaps into a single map
dilepNamesMap = OrderedDict()
dilepNamesMap.update(JES_dilepNamesMap_category)
dilepNamesMap.update(JER_dilepNamesMap)
# dilepNamesMap.update(JMS_dilepNamesMap_category)
# dilepNamesMap.update(JMR_dilepNamesMap_category)
dilepNamesMap.update(btag_dilepNamesMap)
# dilepNamesMap.update(toptag_dilepNamesMap)
dilepNamesMap.update(MET_scale_dilepNamesMap)
dilepNamesMap.update(MET_res_dilepNamesMap)
dilepNamesMap.update(EG_dilepNamesMap)
dilepNamesMap.update(MUON_dilepNamesMap)
dilepNamesMap.update(sys_dilepNamesMap)



sysNames = OrderedDict()
sysNames["jvtSF"] ="jvt"
sysNames["pileupSF"] ="pileup"
# sysNames["lumi"] ="lumi"


sysMap.update(JES_sysMap_category)
sysMap.update(JER_sysMap)
sysMap.update(JMS_sysMap_category)
sysMap.update(JMR_sysMap_category)
sysMap.update(btag_sysMap)
sysMap.update(toptag_sysMap)
sysMap.update(MET_scale_sysMap)
sysMap.update(MET_res_sysMap)
sysMap.update(EG_sysMap)
sysMap.update(MUON_sysMap)
sysMap.update(ttgen_sysMap)
sysMap.update(ttmuF_sysMap)
sysMap.update(ttPDF_sysMap)
sysMap.update(ttNNLO_sysMap)

## Create a list of systematics 

syslist = []
for i in sysMap:
    syslist.append(i)