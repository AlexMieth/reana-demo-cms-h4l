#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_5_3_32/src
eval `scramv1 runtime -sh`
scram b
cd copy-h4l-demo/code/HiggsExample20112012/Level3
cmsRun demoanalyzer_cfg_level3MC.py
