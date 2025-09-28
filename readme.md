## Linkage Synthesis Challenge Problem

This challenge problem is focused on synthesizing planar linkage mechanisms such that a specific output curve is traced using the mechanism. For this project you are tasked with synthesizing linkage mechanisms to trace 6 different output shapes. Further you are tasked with synthesizing mechanisms such that the total material used for the mechanisms in minimized. 

<img src="https://i.ibb.co/qsPC0gC/2021-09-13-0hl-Kleki.png" alt="Numbered Mechanism" border="0">

## Python Requiremnets
we provide three different requirement files:
- `requirements_CPU.txt`: If you do not have GPU use this.
- `requirements_GPU.txt`: If you want to use CUDA GPU use this. (You will also have to adjust the code since it uses CPU by default)
- `requirements_MAC_M.txt`: If you have an M series mac and want to use the M (Metal) series acceleration use this. This is an experimental package so you may just be stuck with the CPU version.

To setup environments first create a new environmnet in conda/mamba:

```bash
conda create --name CP1 python=3.10
```

Then activate the environment and install packages using pip:

```bash
conda activate CP1
pip install -r requirements_CPU.txt
```

how to save changes with git:

1) clear all the outputs (for each notebook)
2) select files to "stage"
3) 'git commit -m "some text"' in terminal
3) 'git push' in terminal


advice from the TA:

1) better initialisation - there is a function provided somehere in the advanced noetbook

2) gradient based  - there is a function provided somehere in the advanced noetbook

3) solution retention - combine from different optimisation

4) d

grediant decent is very bed method - it is first order - 



hat the representation make impact on the BFGS SciPy


To Dos.

1) Generate nice set of mchenism: run the random reneratior for a long time select the best one and save them into the file,
+ run code to take the mechanism form the file ech time it is run 

2) make the code to work for all curves

3) run the Gradien Decent for material and for distance

Patryk: make it work for all curves

Rebecca: try the pipeline GA -> GD distance -> GD meterial 

Further Improvements:
+ the nodes are set to 7, should check if other number of nodes work. Then include all the node # combination
+ adjust randomizer to only generate mechanism with initial state within the d/m constraint
+ optimize the GA/GD parameters: step_size, n_steps, popuation, generation

Angela: try to use the other gradient decent method the TA mentioned
