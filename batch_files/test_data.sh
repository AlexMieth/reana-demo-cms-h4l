#!/bin/bash

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
cd CMSSW_5_3_32/src/reana-demo-cms-h4l/batch_files/
singularity exec -B /eos -B /cvmfs docker://clelange/slc6-cms:latest ./exec_data.sh
