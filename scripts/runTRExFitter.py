#!/usr/bin/env python

import sys
import os
import subprocess
import argparse
from datetime import datetime
from systematics import *
from pathlib import Path

today = datetime.date(datetime.now())


def main():
    # User controlled arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--configdir",      type=str,  default="configs_%s"%today,
                        help="The path to the config files to be used.")
    parser.add_argument("--action",         type=str,  default="hwf",
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
    parser.add_argument("--suff", type=str,  default="",
                        help="suffix added to the outdir and configdir")
    parser.add_argument("--masses", nargs='+', default=['400','500','750','1000','1250','1500','1750','2000','2250','2500','2750','3000','4000','5000'])

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
    masses = args.masses
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
    print ("=====================================================================")

    if 'l' in action:
        raise NotImplementedError()

    # template submission for batch queue - to possibly be changed/improved in the future
    if useBatch == 'pbs':
        templatescript = "scripts/batchScript_template_pbs.sh"
    headdir = os.getcwd()

    date_suffix = configDir[8:] # len("configs_") = 8
    job_dir = f"run/statResults_tt1lep_{date_suffix}"
    
    ttbar_syst_list = []
    twopoint_syst_names = ["tt_muF", "tt_muR", "tt_ISR", "tt_FSR"]
    regions = ["be", "re", "bmu", "rmu"]
    for i in range(1,4):
        for r in regions:
            for s in twopoint_syst_names:
                ttbar_syst_list.append(s+'_'+r+str(i))

    for mass in masses:
        job_name = f"Zprime_{mass}"
        signal_name = f"ZprimeTC2_{mass}"

        if runBONLYFit:
            raise NotImplementedError()
        elif runStatOnly:
            stringForNaming = 'zprime{0}_StatOnly'.format(mass)
            configFileName = "configs/{0}/statonly/zprime_combined_StatOnly.config".format(configDir)
            job_path =  f"{job_dir}/statonly/{job_name}"
            thisCommand = "trex-fitter {0} {1} ".format(action,configFileName)
            newCommand = thisCommand+f" \"Suffix=_statonly:Signal={signal_name}:Job={job_path}\""
            commandList = [newCommand]
            MapOfNamingString = {newCommand:stringForNaming}

            if region != 'combined':
                raise NotImplementedError()
        else:
            commandList = []; MapOfNamingString = {}
            allsys_string = 'zprime{0}_AllSys'.format(mass)
            configFileName = "configs/{0}/allsys/zprime_combined_AllSys.config".format(configDir)
            job_path =  f"{job_dir}/allsys/{job_name}"
            allsys_command = "trex-fitter {0} {1} ".format(action,configFileName)
            if 'r' in action and ranking_indv:
                for sys in ttbar_syst_list: #syslist:
                    allsys_command_ranking = allsys_command+f" \"Ranking={sys}:Signal={signal_name}:Job={job_path}\""
                    commandList.append(allsys_command_ranking)
                    allsys_string_syst = allsys_string.replace("AllSys", sys)
                    MapOfNamingString[allsys_command_ranking] = allsys_string_syst
            else:
                commandList.append(allsys_command + f" \"Signal={signal_name}:Job={job_path}\"")
                MapOfNamingString[allsys_command] = allsys_string

            if region != 'combined':
                raise NotImplementedError()

            if runSeparateSys:
                raise NotImplementedError()
        
        modcommand = "chmod 744 {0}".format(configFileName)
        subprocess.call(modcommand,shell=True)

        for command in commandList:
            if useBatch == "pbs" :
                raise NotImplementedError()
                batchSubmit_PBS(command, MapOfNamingString[command], templatescript, headdir)
            else :
                print("About to call",command)
                breakpoint()
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
