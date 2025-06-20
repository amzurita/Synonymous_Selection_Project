#!/bin/bash

#EDIT THIS LINES:
#$ -N SynSimulations_E5_Selected22Recom6_$JOB_ID.$TASK_ID
#$ -o /u/scratch/a/amzurita/logs/out_SynSimulations_E5_Selected22Recom6_$JOB_ID.$TASK_ID.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l highp
#$ -l group=eeskin
#$ -l h_data=16G
#$ -l time=72:00:00
#$ -m bea

#EDIT THIS LINE WITH THE NUMBER OF SAMPLES (See the trick at the end of the script to count)
#$ -t 1-440

. /u/local/Modules/default/init/modules.sh

/u/project/klohmuel/amzurita/Tools/slim_build/slim -d syn_s=-1e-5 -d recom_rate=1e-6 -d "run_name_output='replicates_E5_Partial_R6_${SGE_TASK_ID}_'" SynSelectionSomeSelected_TaskArray.slim
