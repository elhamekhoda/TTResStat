import ROOT
from array import array, typecodes

histos_1l_path = '/home/schuya/ttres1lepstat/histograms/ttres1l/tt1lep_config_wbtagSR_1b2b/ttRes1L_be1_histos.root'

# histos_1l_path = '/home/schuya/ttres1lepstat/histograms/ttres1l/tt1lep_config_wbtagSR_1b2b/ttRes1L_be1_histos.root'

# histos_1l = ROOT.TFile(histos_1l_path)

# # histos_combined_path = '/home/schuya/ttres1lepstat/histograms/ttres1l2l/ttRes1L2L_be1_histos.root'
# histos_combined_path = '/home/schuya/ttres1lepstat/histograms/ttres1l2l/ttRes1L2L_mllbb_DeltaPhi080to090_histos.root'

# histos_combined = ROOT.TFile(histos_combined_path)

# histos_2l_path = '/home/schuya/ttres1lepstat/data/2l/For_Alex_Thesis/Histograms/ttRes2L_fit_inverted_deltaEta_2dRew_slim_SysAll_V24_mllbb_DeltaPhi080to090_histos.root'

# histos_2l = ROOT.TFile(histos_2l_path)


# h2_up = histos_2l.Get('mllbb_DeltaPhi080to090/ZprimeTC2_1000/JES_EffectiveNP_Statistical2/mllbb_DeltaPhi080to090_ZprimeTC2_1000_JES_EffectiveNP_Statistical2_Up')
# hc_up = histos_combined.Get('mllbb_DeltaPhi080to090/ZprimeTC2_1000/JES_EffectiveNP_Statistical2/mllbb_DeltaPhi080to090_ZprimeTC2_1000_JES_EffectiveNP_Statistical2_Up')
# breakpoint()


# h1_up = histos_1l.Get('be1/diboson/JET_JMS_FF_Shape/be1_diboson_JET_JMS_FF_Shape_Up')
# hc_up = histos_combined.Get('be1/diboson/JET_JMS_FF_Shape/be1_diboson_JET_JMS_FF_Shape_Up')
breakpoint()

# data_histos_path = '/home/schuya/ttres1lepstat/data/1l/fullrun2_aug2022/combined/limit_inputs/be/hist_tt.root'
# data_histos = ROOT.TFile(data_histos_path)



# th_up = trex_histos.Get('be1/tt/jvt/be1_tt_jvt_Up')
# s = ''
# for i in range(1, th_up.GetNbinsX() + 1):
#     s += f"{th_up.GetBinContent(i):.2f} "
# print(f'trex up: {s}')


# th_down = trex_histos.Get('be1/tt/jvt/be1_tt_jvt_Down')
# s = ''
# for i in range(1, th_down.GetNbinsX() + 1):
#     s += f"{th_down.GetBinContent(i):.2f} "
# print(f'trex down: {s}')


# th_shape_up = trex_histos.Get('be1/tt/jvt/be1_tt_jvt_Shape_Up')
# s = ''
# for i in range(1, th_shape_up.GetNbinsX() + 1):
#     s += f"{th_shape_up.GetBinContent(i):.2f} "
# print(f'trex shape up: {s}')


# th_shape_down = trex_histos.Get('be1/tt/jvt/be1_tt_jvt_Shape_Down')
# s = ''
# for i in range(1, th_shape_down.GetNbinsX() + 1):
#     s += f"{th_shape_down.GetBinContent(i):.2f} "
# print(f'trex shape down: {s}')



# dh_up = data_histos.Get('mtt_be1jvtSF__1up')
# # rebin to 400,500,600,700,800,920,1040,1160,1280,1400,1550,1700,1850,2000,2150,2500,3000,3500,4500,6000
# dh_up_rebinned = dh_up.Rebin(19, 'dh_up_rebinned', array('d', [400, 500, 600, 700, 800, 920, 1040,
#                                                                1160, 1280, 1400, 1550, 1700, 1850, 2000, 2150, 2500, 3000, 3500, 4500, 6000]))
# s = ''
# for i in range(1, dh_up_rebinned.GetNbinsX() + 1):
#     s += f"{dh_up_rebinned.GetBinContent(i):.2f} "
# print(f'data up: {s}')


# dh_down = data_histos.Get('mtt_be1jvtSF__1down')
# # rebin to 400,500,600,700,800,920,1040,1160,1280,1400,1550,1700,1850,2000,2150,2500,3000,3500,4500,6000
# dh_down_rebinned = dh_down.Rebin(19, 'dh_down_rebinned', array('d', [400, 500, 600, 700, 800, 920, 1040,
#                                                                      1160, 1280, 1400, 1550, 1700, 1850, 2000, 2150, 2500, 3000, 3500, 4500, 6000]))
# s = ''
# for i in range(1, dh_down_rebinned.GetNbinsX() + 1):
#     s += f"{dh_down_rebinned.GetBinContent(i):.2f} "
# print(f'data down: {s}')
# # print([k.GetName() for k in trex_histos.Get('be1').GetListOfKeys()])
print([k.GetName() for k in histos_1l.Get('be1').Get('ZprimeTC2_1000').GetListOfKeys()])
