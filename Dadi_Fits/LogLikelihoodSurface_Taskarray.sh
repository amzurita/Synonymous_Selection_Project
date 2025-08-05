#!/bin/bash

#EDIT THIS LINES:
#$ -N Likelihood_surfaces_$TASK_ID.$JOB_ID
#$ -o /u/scratch/a/amzurita/logs/out_Likelihood_surfaces_$TASK_ID.$JOB_ID.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l h_data=8G
#$ -l time=24:00:00
#$ -m bea

#Line that makes this a task array
#$ -t 1-20

#Load modules to be used
. /u/local/Modules/default/init/modules.sh
module load anaconda3
#module load gatk/4.2.0.0

conda activate dadienv


#Set up input files
condition_syn_sfs="E5" #PartialE5 0_Recom7, E5_Partial_R7, E5, 0_Recom6, E5_Recom6
condition_dadi_output="E5" #E4_Partial, E4Partial_ZeroSyn, E5_Partial_R7, Zero_Recom7, E5, E5_Partial, Zero_Recom7, E5_Recom6
replicate=$SGE_TASK_ID
num_points=15
suffix="${condition_dadi_output}_Replicate${replicate}"

syn_sfs_file="Summed_SFS/Syn_SFS_DadiInput_${condition_syn_sfs}_Replicate${SGE_TASK_ID}.txt"
input_file_demography="DadiFits_OutputFiles_BugFix/${condition_dadi_output}_TwoEpoch_Replicate${replicate}_two_epoch_demography.txt"

python compute_likelihoodsurface.py \
    --syn_data_file $syn_sfs_file \
    --demography_file $input_file_demography \
    --npts $num_points \
    --suffix $suffix