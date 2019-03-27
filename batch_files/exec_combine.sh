#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_5_3_32/src
eval `scramv1 runtime -sh`
cd copy-h4l-demo/code/HiggsExample20112012/Level3
root -b -l -q ./M4Lnormdatall_lvl3.cc
