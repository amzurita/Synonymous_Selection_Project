#!/bin/bash

#EDIT THIS LINES:
#$ -N DFEInference_European_NeutralDemSynSel$TASK_ID
#$ -o /u/scratch/a/amzurita/logs/out_DFEInference_European_NeutralDemSynSel$TASK_ID.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l h_data=8G
#$ -l time=24:00:00
#$ -m bea
#$ -pe shared 4

#Line that makes this a task array
#$ -t 1-10

#Load modules to be used
. /u/local/Modules/default/init/modules.sh
module load anaconda3
#module load gatk/4.2.0.0

conda activate dadienv

python fit_demography_and_dfe_HumanSims_TwoEpoch_MP.py Summed_SFSs/Syn_SFS_DadiInput_nosel-European-Extended_Replicate$SGE_TASK_ID.txt Summed_SFSs/NonSyn_SFS_DadiInput_synsel-European-Extended_Replicate$SGE_TASK_ID.txt European_NeutralDemSynSel_Extended_Replicate$SGE_TASK_ID