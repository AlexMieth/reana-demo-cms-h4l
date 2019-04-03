#!/bin/bash

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
singularity exec -B /eos -B /cvmfs docker://clelange/slc6-cms:latest ./CMSSW_5_3_32/src/reana-demo-cms-h4l/batch_files/exec_mc.sh
