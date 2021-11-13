import random
import numpy as np
from client import *
import os
import json

key = "iAGHmVKC3ZQTifYA8eCVJPIBfDRCm3ZhO3VOufiHRwTih6BBRj"
pop_size = 10

init_overfit = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

# Validation + Test + Abs(val - test)
def fitness_func(errors):
    return  errors[1] + 0.5 * abs(errors[1] - errors[0])

# Select five pairs of vectors
def selection(population):
    pop_len = len(population)
    errortuple = []
    for i in range(pop_len):
        errors = get_errors(key, population[i])
        theerrortuple = (fitness_func(errors), i)
        errortuple.append(theerrortuple)
    errortuple.sort(key = lambda x: x[0])

    prob = random.randint(0, 1)
    parents = []
    if prob == 0:
        parents.append((population[errortuple[0][1]], population[errortuple[1][1]]))
        parents.append((population[errortuple[0][1]], population[errortuple[2][1]]))
        parents.append((population[errortuple[0][1]], population[errortuple[3][1]]))
        parents.append((population[errortuple[1][1]], population[errortuple[2][1]]))
        parents.append((population[errortuple[1][1]], population[errortuple[3][1]]))
    else:
        parents.append((population[errortuple[1][1]], population[errortuple[0][1]]))
        parents.append((population[errortuple[1][1]], population[errortuple[2][1]]))
        parents.append((population[errortuple[1][1]], population[errortuple[3][1]]))
        parents.append((population[errortuple[0][1]], population[errortuple[2][1]]))
        parents.append((population[errortuple[0][1]], population[errortuple[3][1]]))
    return parents    


def crossover(male, female):
    temp = []
    for i in range(11):
        prob = random.randint(0, 1)
        # print(prob)
        if prob == 0:
            temp.append(male[i])
        else:
            temp.append(female[i])
    return temp

def mutation(person):
    # Return a person
    temp = []
    for j in range(11):
        prob = np.random.randint(0, 100)
        if (prob < 15):
            # print(j)
            dev = abs(person[j])/10
            if random.random() < 0.5:
                # print("yahaan")
                temp.append(person[j] + dev)
            else:
                # print("yahaanasdasdas")
                temp.append(person[j] - dev)
                # self.params[i] += random.uniform(-dev, dev)
            # print(j, len(temp))
            temp[j] = min(10, temp[j])
            temp[j] = max(-10, temp[j])
        else:
            temp.append(person[j])
    return temp

# Read from a file
initial_population = []

for j in range(0, 10):
    gendir = 'iterations/generations_12' + str(j) + '.txt'
    print("GENDIR = ", gendir)
    with open(gendir, 'r') as infile:
        initial_population = json.load(infile)

    selectedpairs = selection(initial_population)

    population = []
    crossover_population = []
    for i in range(len(selectedpairs)):
        child_one = []
        child_two = []
        child_one = crossover(selectedpairs[i][0], selectedpairs[i][1])
        child_two = crossover(selectedpairs[i][1], selectedpairs[i][0])
        crossover_population.append(child_one)
        crossover_population.append(child_two)
        child_one = mutation(child_one)
        child_one = mutation(child_two)
        population.append(child_one)
        population.append(child_two)

    population_with_errors = []

    for i in range(len(population)):
        temp = []
        error = get_errors(key, population[i])
        temp.append(population[i])
        temp.append(error)
        population_with_errors.append(temp)

    if j + 1 == 10:
        write_gendir = 'iterations/generations_130.txt'
        write_errdir = 'errors/generations_130.txt'
        write_seldir = 'selections/generations_130.txt'
        write_crossdir = 'crossover/generations_130.txt'
    else:
        write_gendir = 'iterations/generations_12' + str(j + 1) + '.txt'
        write_errdir = 'errors/generations_12' + str(j + 1) + '.txt'
        write_seldir = 'selections/generations_12' + str(j + 1) + '.txt'
        write_crossdir = 'crossover/generations_12' + str(j + 1) + '.txt'
    print(write_errdir)
    print(write_gendir)
    print(write_seldir)
    print(write_crossdir)
    with open(write_gendir, 'w') as outfile:
        json.dump(population, outfile, indent=2)

    with open(write_errdir, 'w') as outfile:
        json.dump(population_with_errors, outfile, indent=2)

    with open(write_seldir, 'w') as outfile:
        json.dump(selectedpairs, outfile, indent=2)

    with open(write_crossdir, 'w') as outfile:
        json.dump(crossover_population, outfile, indent=2)