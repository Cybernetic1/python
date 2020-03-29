import numpy
import genetic_algorithm
import pickle
import ANN
import matplotlib.pyplot
import time

# Genetic algorithm parameters:
soln_per_pop = 12				# mating pool size (= # parents)
num_parents_mating = 6			# population size
num_generations = 200
mutation_percent = 1			# mutation rate

method = "ReLU"					# neuron's activation function
# method = "sigmoid"

numpy.random.seed(int(time.time()))

import glob
import os

if input("Read old weights file? (enter for yes, 'n' to start new)") != 'n':
	# open the latest weights file:
	list_of_files = glob.glob('/home/yky/python/neuromancer/weights_*')
	latest_file = max(list_of_files, key=os.path.getctime)
	print("Loading file:", latest_file)
	f = open(latest_file, "rb")
	pop_weights_mat = pickle.load(f)
	f.close()
else:
	print("Creating initial population...")
	initial_pop_weights = []
	for curr_sol in numpy.arange(0, soln_per_pop):
		HL1_neurons = 10
		input_HL1_weights = numpy.random.uniform(low=-1.0, high=1.0, 
												 size=(ANN.N, HL1_neurons))
		HL2_neurons = 10
		HL1_HL2_weights = numpy.random.uniform(low=-1.0, high=1.0, 
												 size=(HL1_neurons, HL2_neurons))
		HL3_neurons = 8
		HL2_HL3_weights = numpy.random.uniform(low=-1.0, high=1.0, 
												 size=(HL2_neurons, HL3_neurons))
		output_neurons = ANN.N
		HL3_output_weights = numpy.random.uniform(low=-1.0, high=1.0, 
												  size=(HL3_neurons, output_neurons))

		initial_pop_weights.append(numpy.array([input_HL1_weights, 
													HL1_HL2_weights,
													HL2_HL3_weights,
													HL3_output_weights]))

	pop_weights_mat = numpy.array(initial_pop_weights)

print("pop weights mat shape=", pop_weights_mat.shape)
pop_weights_vector = genetic_algorithm.mat_to_vector(pop_weights_mat)

accuracies = numpy.empty(shape=(num_generations))

for generation in range(num_generations):
	print("Generation : ", generation)

	# converting the solutions from being vectors to matrices.
	pop_weights_mat = genetic_algorithm.vector_to_mat(pop_weights_vector, 
									   pop_weights_mat)

	# Measuring the fitness of each chromosome in the population.
	fitness = ANN.fitness(pop_weights_mat, 
						  activation = method)
	accuracies[generation] = fitness[0]
	print("Fitness")
	print(fitness)

	# Selecting the best parents in the population for mating.
	parents = genetic_algorithm.select_mating_pool(pop_weights_vector, 
									fitness.copy(), 
									num_parents_mating)
	# print("Parents")
	# print(parents)

	# Generating next generation using crossover.
	offspring_crossover = genetic_algorithm.crossover(parents,
									   offspring_size=(pop_weights_vector.shape[0]-parents.shape[0], pop_weights_vector.shape[1]))
	# print("Crossover")
	# print(offspring_crossover)

	# Adding some variations to the offsrping using mutation.
	offspring_mutation = genetic_algorithm.mutation(offspring_crossover, 
									 mutation_percent=mutation_percent)
	# print("Mutation")
	# print(offspring_mutation)

	# Creating the new population based on the parents and offspring.
	pop_weights_vector[0:parents.shape[0], :] = parents
	pop_weights_vector[parents.shape[0]:, :] = offspring_mutation

pop_weights_mat = genetic_algorithm.vector_to_mat(pop_weights_vector, pop_weights_mat)
best_weights = pop_weights_mat [0, :]
acc = ANN.predict_outputs(best_weights, activation = method)
print("Accuracy of the best solution is:", acc)

# print("Weight matrix:\n", pop_weights_mat)

name = str(ANN.N) + "D_10x10x8_" + method
print("Saving file:", name)
f = open("weights_" + name + ".pkl", "wb")
pickle.dump(pop_weights_mat, f)
f.close()

import os
os.system("beep -f 4000 -l 1000")

matplotlib.pyplot.plot(accuracies, linewidth=2, color="red")
matplotlib.pyplot.title("Fig_" + name)
matplotlib.pyplot.xlabel("Iteration", fontsize=12)
matplotlib.pyplot.ylabel("Error", fontsize=12)
if max(accuracies) > 10:
	matplotlib.pyplot.yscale("log")
matplotlib.pyplot.xticks(numpy.arange(0, num_generations+1, 50), fontsize=12)
# matplotlib.pyplot.yticks(numpy.arange(0, 0.01), fontsize=12)
matplotlib.pyplot.savefig("Fig_" + name + ".png")
matplotlib.pyplot.show()
