#!/usr/bin/env python

import sys
import os
import subprocess
import argparse
from datetime import datetime
from systematics import *

today = datetime.date(datetime.now())


def main():
    # User controlled arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--configdir",      type=str,  default="configs_%s"%today,
                        help="The path to the config files to be used.")
    parser.add_argument("--action",         type=str,  default="hwfl",
                        help="The trex-fitter action.")
    parser.add_argument("--excludeSys",            type=str,  default="none",
                        help="List of systematics to exclude from the list.")
    parser.add_argument("--ranking_indv",    dest='ranking_indv', default=True, action='store_true',
                        help="Determines whether to exclude SS systematics or not.")
    parser.add_argument("--runStatOnly",    dest='runStatOnly', default=False, action='store_true',
                        help="Determines whether to include systematics or not.")
    parser.add_argument("--runSeparateSys", dest="runSeparateSys", default=False, action='store_true',
                        help="Determines whether to study effect of single systematic.")
    parser.add_argument("--runBONLYFit", dest="runBONLYFit", default=False, action='store_true',
                        help="Runs the background-only profile likelihood fit")
    parser.add_argument("--region", type=str, default='combined', 
                        help="Determines whether to study signal regions respectively.")
    parser.add_argument('--useBatch',       type=str,        default='pbs',
                        help="Determines whether you will submit fitting to a batch queue. Currently the script is setup only for PBS batch")
    parser.add_argument("--useMorphedSignal",    dest='morphedSignal', default=False, action='store_true',
                        help="Determines whether to use the morphed signal sample or not.")
    parser.add_argument("--suff", type=str,  default="",
                        help="suffix added to the outdir and configdir")

    args = parser.parse_args()
    configDir           = args.configdir+'_'+args.suff
    action              = args.action
    runStatOnly         = args.runStatOnly
    excludeSys          = args.excludeSys
    ranking_indv        = args.ranking_indv
    runSeparateSys      = args.runSeparateSys
    runBONLYFit         = args.runBONLYFit
    region              = args.region
    useBatch            = args.useBatch
    morphedSignal       = args.morphedSignal
    suff                = args.suff

    reg = region



    print ("=====================================================================")
    print ("Executing Run_TRExFitter.py with :")
    print ("configDir        : ",configDir)
    print ("action           : ",action)
    print ("excludeSys       : ",excludeSys)
    print ("runStatOnly      : ",runStatOnly)
    print ("runSeparateSys   : ",runSeparateSys)
    print ("runBONLYFit      : ",runBONLYFit)
    print ("region           : ",region)
    print ("useBatch         : ",useBatch)
    print ("morphedSignal    : ",morphedSignal)
    print ("=====================================================================")

    # make the necessary output directories for storing the results and bookkeeping the configs used
    # os.system("mkdir -p "+outputDir)

    # template submission for batch queue - to possibly be changed/improved in the future
    if useBatch == 'pbs':
        templatescript = "scripts/batchScript_template_pbs.sh"
    # Get current working directory
    headdir = os.getcwd()

    masses = ['400', '500', '750', '1000', '1250', '1500','1750','2000','2250','2500','2750','3000','4000','5000']
    # masses = ['3000', '4000']
    if morphedSignal:
        masses = ['1750','1875','2000','2125','2250','2375','2500','2625','2750','2875','3000','3250','3500','3750','4000','4250','4500','4750','5000','5250','5500','5750','6000']

    if excludeSys == 'none':
        sysToexcl = ''
    else:
        sysToexcl = excludeSys

    ttbar_syst_list = []
    syst_names = ["ttbar_hsShape", "ttbar_hsAcc", "ttbar_hadShape", "ttbar_hadAcc", "ttbar_hdampShape", "ttbar_hdampAcc"]
    twopoint_syst_names = ["tt_muF", "tt_muR", "tt_ISR", "tt_FSR"]
    regions = ["be", "re", "bmu", "rmu"]
    for i in range(1,4):
        for r in regions:
            for s in twopoint_syst_names:
                ttbar_syst_list.append(s+'_'+r+str(i))

    for mass in masses:
        if runBONLYFit:
            allsys_string = 'zprime{0}_BONLY_AllSys'.format(mass)
            configFileName = "configs/{0}/allsys/zprime{1}_combined_BONLY_AllSys.config".format(configDir,mass)
            allsys_command = "trex-fitter {0} {1}".format(action,configFileName)
            commandList = [allsys_command]
            MapOfNamingString = {allsys_command:allsys_string}

            # fitblind_string = 'zprime{0}_BONLY_FitBlind'.format(mass)
            # configFileName = "configs/{0}/allsys/zprime{1}_combined_BONLY_FitBlind.config".format(configDir,mass)
            # fitblind_command = "trex-fitter {0} {1}".format(action,configFileName)
            # commandList += [fitblind_command]
            # MapOfNamingString[fitblind_command] = fitblind_string

        elif runStatOnly:
            stringForNaming = 'zprime{0}_StatOnly'.format(mass)
            configFileName = "configs/{0}/statonly/zprime{1}_combined_StatOnly.config".format(configDir,mass)
            thisCommand = "trex-fitter {0} {1} ".format(action,configFileName)
            newCommand = thisCommand+" \"Suffix=_statonly\""
            commandList = [newCommand]
            MapOfNamingString = {newCommand:stringForNaming}

            #stringForNaming = 'zprime{0}_MCstat'.format(mass)
            #configFileName = "configs/{0}/MCstat/zprime{1}_combined_MCstat.config".format(configDir,mass)
            #newCommand = "trex-fitter {0} {1}  \"Systematics=none:Suffix=_MCstat\"".format(action,configFileName)
            #commandList += [newCommand]
            #MapOfNamingString[newCommand] = stringForNaming

            #fitblind_string = 'zprime{0}_StatOnly_FitBlind'.format(mass)
            #configFileName = "configs/{0}/statonly/zprime{1}_combined_StatOnly_FitBlind.config".format(configDir,mass)
            #fitblind_command = "trex-fitter {0} {1}".format(action,configFileName)
            #commandList += [fitblind_command]
            #MapOfNamingString[fitblind_command] = fitblind_string

            if region != 'combined':
                commandList = []; MapOfNamingString = {}
                newCommand = thisCommand+" \"Regions={0}:Suffix=_statonly_{1}\"".format(reg,reg)
                newString = stringForNaming.replace("StatOnly","StatOnly_"+reg)
                commandList.append(newCommand)
                MapOfNamingString[newCommand]=newString

        else:
            commandList = []; MapOfNamingString = {}
            allsys_string = 'zprime{0}_AllSys'.format(mass)
            configFileName = "configs/{0}/allsys/zprime{1}_combined_AllSys.config".format(configDir,mass)
            allsys_command = "trex-fitter {0} {1} ".format(action,configFileName)
            if 'r' in action and ranking_indv:
                for sys in ttbar_syst_list: #syslist:
                    allsys_command_ranking = allsys_command+" \"Ranking={0}\"".format(sys)
                    commandList.append(allsys_command_ranking)
                    allsys_string_syst = allsys_string.replace("AllSys", sys)
                    MapOfNamingString[allsys_command_ranking] = allsys_string_syst
            else:
                commandList.append(allsys_command)
                MapOfNamingString[allsys_command] = allsys_string

            # fitblind_string = 'zprime{0}_FitBlind'.format(mass)
            # configFileName = "configs/{0}/allsys/zprime{1}_combined_FitBlind.config".format(configDir,mass)
            # fitblind_command = "trex-fitter {0} {1}".format(action,configFileName)
            # commandList += [fitblind_command]
            # MapOfNamingString[fitblind_command] = fitblind_string

            if region != 'combined':
                commandList = []; MapOfNamingString = {}

                allsys_command_reg = allsys_command+" \"Regions={0}:Suffix=_{1}\"".format(reg,reg)
                allsys_string_reg = allsys_string+'_'+reg
                commandList.append(allsys_command_reg)
                MapOfNamingString[allsys_command_reg] = allsys_string_reg

                fitblind_command_reg = fitblind_command+" \"Regions={0}:Suffix=_{1}\"".format(reg,reg)
                fitblind_string_reg = fitblind_string+'_'+reg
                commandList.append(fitblind_command_reg)
                MapOfNamingString[fitblind_command_reg]=fitblind_string_reg

            if runSeparateSys:
                for sys in sysToexcl:
                    if 'r' in action:
                        newCommand = thisCommand+" \"Ranking={0}\"".format(sys)
                    else:
                        newCommand = thisCommand+" \"Exclude={0}:Suffix=_exclude_{1}\"".format(sys,sys)
                    newString = stringForNaming.replace('AllSys',sys)
                    commandList.append(newCommand)
                    MapOfNamingString[newCommand]=newString



        modcommand = "chmod 744 {0}".format(configFileName)
        subprocess.call(modcommand,shell=True)

        for command in commandList:
            if useBatch == "pbs" :
                batchSubmit_PBS(command, MapOfNamingString[command], templatescript, headdir)
            else :
                print("About to call",command)
                subprocess.call(command, shell=True)

def batchSubmit_PBS(command, stringForNaming, templatescript, headdir) :
    # Perform setLimitsOneMassPoint on batch
    batch_files = "{0}/batch_files".format(headdir)
    os.system("mkdir -p "+batch_files)

    log_path = "{0}/batch_files/logs".format(headdir)
    os.system("mkdir -p "+log_path)

    batchcommand = command
    print(batchcommand)

    # Open batch script as fbatchin
    fbatchin = open(templatescript, 'r')
    fbatchindata = fbatchin.read()
    fbatchin.close()

    # open modified batch script (fbatchout) for writing
    batchtempname = '{0}/TRExFitter_{1}.sh'.format(batch_files,stringForNaming)
    fbatchout = open(batchtempname,'w')
    fbatchoutdata = fbatchindata.replace("LOGFILE_PATH",log_path)
    fbatchoutdata = fbatchoutdata.replace("RUNDIR",headdir) # In batch script replace YYY for path for whole package
    fbatchoutdata = fbatchoutdata.replace("RUN_COMMAND",batchcommand) # In batch script replace ZZZ for submit command
    fbatchout.write(fbatchoutdata)
    modcommand = 'chmod 744 {0}'.format(batchtempname)
    subprocess.call(modcommand, shell=True)
    fbatchout.close()
    
    submitcommand = "qsub -V -N %s %s"%(stringForNaming, batchtempname)
    print(submitcommand)
    subprocess.call(submitcommand, shell=True)
  
# when calling this script
if __name__ == "__main__":
    main()
