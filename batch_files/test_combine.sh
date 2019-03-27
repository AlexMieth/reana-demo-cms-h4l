#!/bin/bash

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
singularity exec -B /eos -B /cvmfs docker://clelange/slc6-cms:latest ./exec_combine.sh
