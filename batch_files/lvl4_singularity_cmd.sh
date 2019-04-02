export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
echo "exported SINGULARITY_CACHEDIR"
singularity exec -B /eos -B /cvmfs docker://clelange/slc6-cms:latest ./exec_lvl4_stage1.sh $1
echo "Ran singularity cmd with argument:"
echo $1
