# Simulations Code

Simulations were run on SLiM version 3.7.1. Scripts are as follows:
* **SynSelection_TaskArray.slim**: SLiM simulation where all synonymous mutations experience a selection coefficient, s. The selection coefficient, _s_, and the recombination rate, _r_, are specified as input parameters.
* **SynSelectionSomeSelected_TaskArray.slim**: SLiM simulation where 22% of synonymous mutations experience a selection coefficient, _s_. The selection coefficient, _s_, and the recombination rate, _r_, are specified as input parameters.
* **TaskArray_[]**: Bash script used to submit the simulation tasks to the cluster. Name indicates the selection model used. Recombination was changed to generate simulations under different r parameters.
