#!/bin/bash
cd ../
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
scram b
cd Level3/
cmsRun demoanalyzer_cfg_level3MC.py
