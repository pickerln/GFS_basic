import time
import numpy as np
import matplotlib.pyplot as plt

from GeneticAlgorithm import GeneticAlgorithm

# Number of chromosomes in a population, must be even
M = 6
N = 10
MaxGen = 10000
Pc = .90
Pm = .3
Er = .3
Ub = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100])
Lb = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# t to track the time it takes to train
tic = time.perf_counter()

ga = GeneticAlgorithm(M, N, MaxGen, Pc, Pm, Er, Ub, Lb)
best_chromosome, fitness_over_time = ga.run()

toc = time.perf_counter()
tt = (toc - tic)

print("time to run: ", tt, " sec")

generations_array = np.arange(0, MaxGen, 1)

plt.plot(generations_array, fitness_over_time)
plt.title('Best Fitness over time')
plt.show()