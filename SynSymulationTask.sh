#!/bin/bash

#EDIT THIS LINES:
#$ -N SynSimulation
#$ -o /u/scratch/a/amzurita/logs/out_SynSimulation.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l highp
#$ -l h_data=16G
#$ -l time=24:00:00
#$ -m bea

#Load modules to be used
. /u/local/Modules/default/init/modules.sh
#module load anaconda3
#module load gatk/4.2.0.0


/u/project/klohmuel/amzurita/Tools/slim_build/slim SynSelection.slim
