#!/bin/bash

#EDIT THIS LINES:
#$ -N DFEInference_E5_Partial
#$ -o /u/scratch/a/amzurita/logs/out_DFEInference_E5_Partial.txt

#$ -j y
#$ -cwd
#$ -M amzurita
#$ -l highp
#$ -l group=eeskin
#$ -l h_data=8G
#$ -l time=48:00:00
#$ -m bea
#$ -pe shared 4

#Load modules to be used
. /u/local/Modules/default/init/modules.sh
module load anaconda3
#module load gatk/4.2.0.0

conda activate dadienv

python fit_demography_and_dfe_E5_Partial_MP.py Summed_SFS/Syn_SFS_DadiInput_Selected22_E5.txt Summed_SFS/NonSyn_SFS_DadiInput_Selected22_E5.txt E5_TwoEpoch_Partial_SmallInitial
