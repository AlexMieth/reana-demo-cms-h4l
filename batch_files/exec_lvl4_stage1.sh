cd CMSSW_5_3_32/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval 'scramv1 runtime -sh'
scram b
cd reana-demo-cms-h4l/code/HiggsExample20112012/Level4
cmsRun ./cfg_files/demoanalyzer_cfg$1.py
