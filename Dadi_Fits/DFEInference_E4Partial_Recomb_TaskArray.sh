#!/bin/bash

#EDIT THIS LINES:
#$ -N DFEInference_E4Partial_Recomb7$TASK_ID
#$ -o /u/scratch/a/amzurita/logs/out_DFEInference_E4Partial_Recomb7$TASK_ID.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l h_data=8G
#$ -l time=24:00:00
#$ -m bea
#$ -pe shared 4

#Line that makes this a task array
#$ -t 1-20

#Load modules to be used
. /u/local/Modules/default/init/modules.sh
module load anaconda3
#module load gatk/4.2.0.0

conda activate dadienv

python fit_demography_and_dfe_E5_TwoEpoch_MP.py Summed_SFS/Syn_SFS_DadiInput_E4_Partial_R7_Replicate$SGE_TASK_ID.txt Summed_SFS/NonSyn_SFS_DadiInput_E4_Partial_R7_Replicate$SGE_TASK_ID.txt E4_Partial_R7_TwoEpoch_Replicate$SGE_TASK_ID
