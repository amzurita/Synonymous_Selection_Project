#!/bin/bash

#EDIT THIS LINES:
#$ -N SynSimulations_E4_$JOB_ID.$TASK_ID
#$ -o /u/scratch/a/amzurita/logs/out_SynSimulations_E4_$JOB_ID.$TASK_ID.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l highp
#$ -l h_data=16G
#$ -l time=48:00:00
#$ -m bea

#EDIT THIS LINE WITH THE NUMBER OF SAMPLES (See the trick at the end of the script to count)
#$ -t 1-30

. /u/local/Modules/default/init/modules.sh

/u/project/klohmuel/amzurita/Tools/slim_build/slim -d syn_s=10e-4 "run_name_output='E4_$SGE_TASK_ID'" SynSelection_TaskArray.slim