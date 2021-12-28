import numpy as np
import random


class GeneticAlgorithm:
    """ M ------- size of population, must be even
        N ------- number of genes in a chromosome
        MaxGen -- maximum number of generations to run for
        Pc ------ probability of crossover
        pm ------ probability of mutation
        obj ----- name of fitness function
        ub ------ vector of upper bounds for the genes
        lb ------ vector of lower bounds for the genes
    """

    def __init__(self, m, n, maxgen, pc, pm, er, ub, lb, fitness_function, chromosome_to_include=[],
                 mutate_percent=False, mutate_percentage=.01, pop_to_include=[], view_gen=False):
        self.cgcurve = np.zeros(maxgen)
        self.m = m
        self.n = n
        self.maxgen = maxgen
        self.pc = pc
        self.pm = pm
        self.mutate_percentage = mutate_percentage
        self.mutate_high = 1 + mutate_percentage
        self.mutate_low = 1 - mutate_percentage
        self.er = er
        self.ub = ub
        self.lb = lb
        self.view_gen = view_gen
        self.chromosome_to_include = chromosome_to_include
        if pop_to_include == []:
            self.population = self.initialization()
        else:
            self.population = pop_to_include
        self.fitness_function = fitness_function
        self.population = self.fitness_function(self.population)
        self.mutate_percent = mutate_percent

    def initialization(self):
        # Last 'gene' is the fitness value
        population = np.random.rand(self.m, self.n + 1)
        population[:, :-1] = (self.ub - self.lb) * population[:, :-1] + self.lb
        # that last column make it 0 for the starting fitness value
        population[:, -1] = np.zeros((1, self.m))
        if self.chromosome_to_include:
            population[0] = self.chromosome_to_include
        return population

    def mutate(self, child):
        # An np array full of mutations
        mutates = (self.ub - self.lb) * np.random.rand(1, self.n) + self.lb
        # HAlf of the time we mutate higher, half the time we mutate lower
        if self.mutate_percent:
            R = np.random.rand()
            if R < .5:
                mutates = self.mutate_low * child[:-1]
            else:
                mutates = self.mutate_high * child[:-1]

        # Create array of 1s and 0s for true/ false within prob mutation
        check_pm = (np.random.rand(1, self.n) < self.pm).astype(int)

        # No need to mutate fitness value
        mutates = np.append(mutates, [0])
        check_pm = np.append(check_pm, [0])
        child = check_pm * mutates + (1 - check_pm) * child

        return child

    def elitism(self, population, new_population):
        # number of elite chosen here
        elite_no = round(self.m * self.er)
        sorted_population = population[population[:, -1].argsort()]
        # Keep best from old population
        new_population[-elite_no:, :] = sorted_population[-elite_no:, :]
        return new_population

    def single_cross(self, parent1, parent2):
        # Single point crossover Using vectors
        gene_no = self.n + 1
        cros_pt = random.randint(1, gene_no - 2)
        # if greater than the probability of crossover, it remains the original
        # parent
        r1 = random.uniform(0, 1)
        if r1 >= self.pc:
            child1 = parent1
        else:
            child1 = np.append(parent1[0: cros_pt], parent2[cros_pt:gene_no])

        r2 = random.uniform(0, 1)
        if r2 >= self.pc:
            child2 = parent2
        else:
            child2 = np.append(parent2[0: cros_pt], parent1[cros_pt:gene_no])

        return child1, child2

    def selection(self, population):
        # Sort by fitness values
        sorted_population = population[population[:, -1].argsort()[::-1]]
        # fitness scaling
        sum_fitness_values = np.sum(population[:, -1])
        norm_sorted_population = np.copy(sorted_population)
        norm_sorted_population[:, -1] /= sum_fitness_values

        # Get cumulative sum of fitness values
        chrom_idexs = np.arange(0, self.m, 1)
        # initialize cumulative fitness values vector
        cumsum = np.zeros(self.m)
        for i in chrom_idexs:
            for j in np.arange(i, self.m, 1):
                cumsum[i] += norm_sorted_population[j][-1]

        # Use random number to pick parent number 1
        r = random.uniform(0, 1)
        parent1_idx = self.m - 1
        for i in chrom_idexs:
            if r > cumsum[i]:
                parent1_idx = i - 1
                break

        parent2_idx = parent1_idx
        # to break the while loop in rare cases where we keep getting the same index
        while_loop_stop = 0
        while parent2_idx == parent1_idx:
            while_loop_stop += 1
            r = random.uniform(0, 1)
            if while_loop_stop > 20:
                break
            for i in chrom_idexs:
                if r > cumsum[i]:
                    parent2_idx = i - 1
                    break

        parent1 = sorted_population[parent1_idx]
        parent2 = sorted_population[parent2_idx]

        return parent1, parent2

    # @staticmethod
    # def fitness_function(population):
    #     """
    #     User defined fitness function
    #     -- This is a dummy fit func
    #     """
    #     population[:, -1] = np.min(1/abs(population[:, :-1]/10 - 1), axis=1)
    #     return population

    def run(self):
        if self.view_gen:
            print('Generation # ', 0)
        self.cgcurve[0] = np.max(self.population[:, -1])
        population = self.population

        # Main loop
        for g in np.arange(1, self.maxgen, 1):
            if self.view_gen:
                print()
                print('Generation # ', g)

            # Calculate the fitness values
            population = self.fitness_function(population)

            # Empty array for next population
            new_population = np.zeros((self.m, self.n + 1))
            for k in np.arange(0, self.m, 2):
                # Selection
                [parent1, parent2] = self.selection(population)

                # Crossover
                [child1, child2] = self.single_cross(parent1, parent2)

                # Mutation
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                new_population[k] = child1
                new_population[k + 1] = child2

            new_population = self.fitness_function(new_population)

            # Elitism
            population = self.elitism(population, new_population)

            self.cgcurve[g] = np.max(population[:, -1])

        sort_final_pop = population[population[:, -1].argsort()[::-1]]
        best_chrom = sort_final_pop[0]

        return best_chrom, population, self.cgcurve
