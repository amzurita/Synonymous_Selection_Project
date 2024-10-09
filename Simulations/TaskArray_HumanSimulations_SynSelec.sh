#!/bin/bash

#EDIT THIS LINES:
#$ -N HumanSimulations_SynSel_$JOB_ID.$TASK_ID
#$ -o /u/scratch/a/amzurita/logs/out_HumanSimulations_SynSel_$JOB_ID.$TASK_ID.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l highp
#$ -l h_data=16G
#$ -l time=72:00:00
#$ -m bea

#EDIT THIS LINE WITH THE NUMBER OF SAMPLES (See the trick at the end of the script to count)
#$ -t 1-2000

. /u/local/Modules/default/init/modules.sh

/u/project/klohmuel/amzurita/Tools/slim_build/slim -d "run_name_output='humansim_synsel_extendedreplicate${SGE_TASK_ID}'" HumanPopSynSelection.slim
