#!/bin/bash

#EDIT THIS LINES:
#$ -N DFEInference_E4_Recomb6
#$ -o /u/scratch/a/amzurita/logs/out_DFEInference_E4_Recomb6.txt

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

python fit_demography_and_dfe_E5_TwoEpoch_MP.py Summed_SFS/Syn_SFS_DadiInput_Selected22_Recom6_E4.txt Summed_SFS/NonSyn_SFS_DadiInput_Selected22_Recom6_E4.txt E4_TwoEpoch_Sel22Recom6
