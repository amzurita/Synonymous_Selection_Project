#!/bin/bash

#EDIT THIS LINES:
#$ -N DFEInference_E5
#$ -o /u/scratch/a/amzurita/logs/out_DFEInference_E5.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l highp
#$ -l group=eeskin
#$ -l h_data=16G
#$ -l time=48:00:00
#$ -m bea

#Load modules to be used
. /u/local/Modules/default/init/modules.sh
module load anaconda3
#module load gatk/4.2.0.0

conda activate dadienv

python fit_demography_and_dfe_E5_TwoEpoch_Outputll.py Summed_SFS/Syn_SFS_DadiInput_E5.txt Summed_SFS/NonSyn_SFS_DadiInput_E5.txt E5_TwoEpoch_Outputll