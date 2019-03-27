#!/bin/bash
cd ../../
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd reana-demo-cms-h4l/Level3/
root -b -l -q ./M4Lnormdatall_lvl3.cc
