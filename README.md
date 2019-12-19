#  CPS783 - Metaheuriscs for Optimization<br/> Adaptive Large Neighborhood Search - Maximally Diverse Grouping Problem (MDGP)

This repository refers to the final work of the discipline: **CPS783 - Metaheuriscs for Optimization**, PESC / COPPE / UFRJ , taught by Professor [Laura Bahiense](https://www.cos.ufrj.br/index.php/pt-BR/telefones-do-pesc/details/3/2566) during the third quarter of 2019.


**Students:**

* [Márcio William](https://github.com/suwilliam-nit)
* [Marcos Aurélio C de S Filho](https://github.com/Maasouza)
* [Rafael G Damasceno](https://github.com/DamascenoRafael)


## About

The purpose of this repository is to establish and evaluate the implementation of an Adaptive Large Neighborhood Search (ALNS) metaheuristic, applied to the Maximally Diverse Grouping Problem (MDGP). Techniques covered include the operation of an ALNS, a reheated Simulated Annealing framework, and the use of the Path-Relinking strategy.


## Running algorithm

All algorithms are written using [Python 3](https://www.python.org/) and are available in the `src` directory. The only external package used was [NumPy](https://numpy.org/).

The algorithm can be run through the file `src/main.py`, where there are comments explaining how to select the problems and choose the different parameters.

In the `data` directory you can find some problems that can be executed by the algorithms. The `output` folder will store the algorithm execution results.

In the `src/notebooks for plotting` folder are the [Jupyter Notebook](https://jupyter.org/) files that can be used to plot the results.

## Outputs

- Execution Summary Output  
Format:  
`info_<<intance name>>.info` or  
`info_reheat_<<instance name>>.info`
            
            Instancia: Instance Name
                Avg exec time: 1234.56 
                Avg time to find best: 123.45
                Avg exec itts: 1000
                Avg itts to find best: 100
            Best Solutions:
                Max: 12345.678 on itt: 123
                Min: 10000.000
                Avg: 1234.567
                StdDev: 123.45

- Single Execution Output  
Format:  
`run_<<intance name>>_<<itteration>>.out` or  
`reheat_run_<<intance name>>_<<itteration>>.out`

            Instancia: Instance Name
            Execution time: 123.456
            Best solution: 123456.789 at itteration 123/1234
            Removal Operators Weight
                Random - 123
                Biased Random - 123
                Greedy Least Contributor - 123
                Pair Shaw - 123
                Shaw - 123
            Insertion Operators Weight
                Random - 123
                greedy mean diversity max - 123
                greedy mean diversity min - 123
                greedy mean diversity best group max - 123 
                greedy mean diversity best group min - 123
                worst regret - 123 

- Single Execution Best Results  
Format:  
`run_itts_and_bests_<<intance name>>_<<itteration>>.out` or
`reheat_run_itts_and_bests_<<intance name>>_<<itteration>>.out`

            itt_0 best_0
            itt_1 best_1
            .
            .
            .
            itt_n best_n

