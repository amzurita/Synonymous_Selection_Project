#!/bin/bash

#EDIT THIS LINES:
#$ -N DFEInference_E5_Partial
#$ -o /u/scratch/a/amzurita/logs/out_DFEInference_E5_Partial.txt

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

python fit_demography_and_dfe.py Summed_SFS/Syn_SFS_DadiInput_E5_Selected22.txt Summed_SFS/NonSyn_SFS_DadiInput_E5_Selected22.txt E5_TwoEpoch_Partial
