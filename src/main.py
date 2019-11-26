from simulation import *
from instance import *
from solution import *


if __name__ == "__main__":
    instance = Instance('../data/mdgplib/Geo/Geo_n010_ds_01.txt')
    alns = ALNS(instance)
    alns.generate_random_solution()
    print(alns.current_solution)

