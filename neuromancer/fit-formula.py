# -*- coding: utf8 -*-

# TO-DO:
# * ability to add custom formula to population
# * GUI params not passed back to main module
# * stop the search, restart
# * output text explanation of formula files
# * able to browse formulas in GUI
# * cache? What's that?

# SOLVED:
# * the best formula may not be present in the latest population, but some of his "look-alikes" will
# * appearance of complex numbers was due to (-1)**fraction
# * can print formulas while running
# * now able to re-insert 'best' guy back to population

import random
import operator
import math
import pygame
import pickle
import os			# for beep

import sys
sys.setrecursionlimit(8000)

# Algorithm configuration; These numbers should be copied to GUI
max_gens = 200
max_depth = 6
pop_size = 300
bouts = 5
p_repro = 0.02
p_cross = 0.80
p_mut = 0.06

population = []
best = {'fitness': float('inf')}

def op_squared(x):
	return x*x

def op_cubed(x, n):
	return x**3

# problem configuration
terms = ['x', 'y', 'R']

funcs = [
	operator.add,
	operator.sub,
	operator.mul,
	operator.truediv,
	math.exp,
	math.sqrt,
	op_squared
	]

arity = {
	operator.add: 2,
	operator.sub: 2,
	operator.mul: 2,
	operator.truediv: 2,
	math.exp: 1,
	math.sqrt: 1,
	op_squared: 1,
	op_cubed: 1
	}

symbol = {
	operator.add: '+',
	operator.sub: '-',
	operator.mul: '*',
	operator.truediv: '/',
	math.exp: 'e^',
	math.sqrt: 'sqrt',
	op_squared: '^2',
	op_cubed: '^3'
	}

def rand_in_bounds(min, max):
	return random.uniform(min, max)

def export_tree_as_graph(node, fname):
	f = open(fname, 'w')
	f.write("digraph {\n")
	# f.write("fontname=\"times-bold\";")
	print_tree_as_graph(f, node)
	f.write("}\n")
	f.close()

def print_tree_as_graph(f, node, index = 0):
	if not isinstance(node, list):
		if isinstance(node, float):
			f.write("node" + str(index) + "[label=\"" + str(round(node, 2)) + "\",style=\"filled\",fillcolor=\"yellow\"];\n")
		elif node == "E20" or node == "E100" or node == "Avg":
			f.write("node" + str(index) + "[label=\"" + str(node) + "\",style=\"filled\",fillcolor=\"#FFCCCC\"];\n")
		else:
			f.write("node" + str(index) + "[label=\"" + str(node) + "\"];\n")
		return 1
	op = node[0]
	color = "\"];\n"
	if op == operator.and_ or op == operator.or_:
		color = "\",color=\"red\"];\n"
	elif op == operator.gt or op == operator.lt:
		color = "\",color=\"green\"];\n"
	else:
		color = "\",color=\"red\"];\n"
	f.write("node" + str(index) + "[label=\"" + symbol[node[0]] + color)
	f.write("node" + str(index) + " -> node" + str(index + 1) + ";\n")
	count1 = print_tree_as_graph(f, node[1], index + 1)
	if arity[node[0]] == 2:
		f.write("node" + str(index) + " -> node" + str(index + count1 + 1) + ";\n")
		count2 = print_tree_as_graph(f, node[2], index + count1 + 1)
		return count1 + count2 + 1
	return count1 + 1

def save_population(fname):
	global population
	f = open(fname, 'wb')
	pickle.dump(population, f, pickle.HIGHEST_PROTOCOL)
	f.close()
	print("Population saved")

def load_population(fname):
	global population
	f = open(fname, 'rb')
	population = pickle.load(f)
	f.close()
	print("Population loaded")

def print_program(node):
	if not isinstance(node, list):
		if isinstance(node, float):
			return str(round(node, 2))
		else:
			return node
	if arity[node[0]] == 1:
		if symbol[node[0]][0] == '^':
			return "(" + print_program(node[1]) + symbol[node[0]] + ")"
		return symbol[node[0]] + "(" +  print_program(node[1]) + ")"
	return "(" + print_program(node[1]) + symbol[node[0]] + print_program(node[2]) + ")"

def eval_program(node, dict):
	if not isinstance(node, list):
		if isinstance(node, float):
			return node
		if dict[node] is not None:
			return dict[node]
		return node
	arg1 = eval_program(node[1], dict)
	if arity[node[0]] == 1:
		try:
			return node[0](arg1)
		except:
			return float('nan')
	arg2 = eval_program(node[2], dict)
	if node[0] == operator.truediv and arg2 == 0.0:
		return float('nan')
	try:
		return node[0](arg1, arg2)
	except:
		return float('nan')

def generate_random_program(max, depth = 0):
	if (depth == max - 1) or (depth > 1 and random.uniform(0.0,1.0) < 0.1):
		t = terms[random.randint(0, len(terms) - 1)]
		if t == 'R':
			return rand_in_bounds(-5.0, +5.0)
		else:
			return t
	depth += 1
	func = funcs[random.randint(0, len(funcs) - 1)]
	arg1 = generate_random_program(max, depth)
	if arity[func] == 2:
		arg2 = generate_random_program(max, depth)
		return [func, arg1, arg2]
	return [func, arg1]

def count_nodes(node):
	if not isinstance(node, list):
		return 1
	a1 = count_nodes(node[1])
	if arity[node[0]] == 2:
		a2 = count_nodes(node[2])
		return a1 + a2 + 1
	return a1 + 1

def tournament_selection(pop, bouts):
	selected = []
	# print("bouts = ", bouts
	for i in range(0, bouts):
		selected.append(pop[random.randint(0, len(pop) - 1)])
	return sorted(selected, key = lambda x: x['fitness'])[0]

def replace_node(node, replacement, node_num, cur_node = 0):
	if cur_node == node_num:
		return [replacement, (cur_node + 1)]
	cur_node += 1
	if not isinstance(node, list):
		return [node, cur_node]
	a1, cur_node = replace_node(node[1], replacement, node_num, cur_node)
	if arity[node[0]] == 2:
		a2, cur_node = replace_node(node[2], replacement, node_num, cur_node)
		return [[node[0], a1, a2], cur_node]
	else:
		return [[node[0], a1], cur_node]

def copy_program(node):
	# print(node
	if not isinstance(node, list):
		return node
	if arity[node[0]] == 1:
		return [node[0], copy_program(node[1])]
	return [node[0], copy_program(node[1]), copy_program(node[2])]

def get_node(node, node_num, current_node = 0):
	if current_node == node_num:
		return node, (current_node + 1)
	current_node += 1
	if not isinstance(node, list):
		return [], current_node
	a1, current_node = get_node(node[1], node_num, current_node)
	if a1:		# a1 != []
		return a1, current_node
	if arity[node[0]] == 2:
		a2, current_node = get_node(node[2], node_num, current_node)
		if a2:
			return a2, current_node
	return [], current_node

def prune(node, max_depth, depth = 0):
	if depth == max_depth - 1:
		t = terms[random.randint(0, len(terms) - 1)]
		if t == 'R':
			return rand_in_bounds(-5.0, +5.0)
		else:
			return t
	depth += 1
	if not isinstance(node, list):
		return node
	a1 = prune(node[1], max_depth, depth)
	if arity[node[0]] == 2:
		a2 = prune(node[2], max_depth, depth)
		return [node[0], a1, a2]
	return [node[0], a1]

def crossover(parent1, parent2, max_depth):
	pt1, pt2 = random.randint(1, count_nodes(parent1) - 1), \
		random.randint(1, count_nodes(parent2) - 1)
	# print("pt 1 & 2 = ", pt1, pt2
	tree1, c1 = get_node(parent1, pt1)
	tree2, c2 = get_node(parent2, pt2)
	# print("tree 1 & 2 = ", tree1, tree2
	child1, c1 = replace_node(parent1, copy_program(tree2), pt1)
	child1 = prune(child1, max_depth)
	child2, c2 = replace_node(parent2, copy_program(tree1), pt2)
	child2 = prune(child2, max_depth)
	return [child1, child2]

def mutation(parent, max_depth):
	random_tree = generate_random_program(max_depth / 2)
	point = random.randint(0, count_nodes(parent) - 1)
	child, count = replace_node(parent, random_tree, point)
	child = prune(child, max_depth)
	return child

def fitness(program, num_trials = 30):
	# print("prog=", print_program(program))
	sum_error = 0.0
	for i in range(1, num_trials):
		x = rand_in_bounds(0.0, 2.0)
		# diagonal value:
		error = eval_program(program, {'x': x, 'y': x}) - 1.0
		sum_error += abs(error)
		# x- and y- axis value:
		z = 2.0 / (1.0 + math.exp(80.0 * (x - 0.05))) - 1.0
		error = eval_program(program, {'x': x, 'y': 0.0}) - z
		sum_error += abs(error)
		error = eval_program(program, {'x': 0.0, 'y': x}) - z
		sum_error += abs(error)
	return sum_error / num_trials

def search(again=False):
	global population, best

	if (not again):
		print("Initializing population...")

		population = []
		for i in range(0, pop_size):
			prog = generate_random_program(max_depth)
			population.append({'prog' : \
				prog, \
				'fitness' : \
				fitness(prog)})

		population.sort(key = lambda x: 1e99 if math.isnan(x['fitness']) else x['fitness'])
		GUI.best = best = population[0]
		GUI.plot_population(population)
		# input("Press any key to continue....")
	else:
		print("Retaining population...")
		print("size =", len(population))
		# print("\tlast best formula =", end='')
		# print(print_program(best['prog']))
		# print("\tbest fitness =", best['fitness'])
		p0 = population[0]
		print("\tbest population formula =", end='')
		print(print_program(p0['prog']))
		print("\tbest population fitness =", p0['fitness'])

	for gen in range(0, max_gens):
		# print "\nGenerating children..."
		children = []
		while len(children) < pop_size:
			operation = random.uniform(0.0, 1.0)
			p1 = tournament_selection(population, bouts)
			c1 = {}
			if operation < p_repro:
				c1['prog'] = copy_program(p1['prog'])
			elif operation < p_repro + p_cross:
				p2 = tournament_selection(population, bouts)
				c2 = {}
				c1['prog'],c2['prog'] = crossover(p1['prog'], p2['prog'], max_depth)
				children.append(c2)
			elif operation < p_repro + p_cross + p_mut:
				c1['prog'] = mutation(p1['prog'], max_depth)

		# print "Evaluating children..."
		if len(children) < pop_size:
			children.append(c1)
		for c in children:
			c['fitness'] = fitness(c['prog'])
		population = children
		population.sort(key = lambda x: 1e99 if math.isnan(x['fitness']) else x['fitness'])

		GUI.plot_population(population)

		if population[0]['fitness'] <= best['fitness']:
			GUI.best = best = population[0]
			os.system("beep -f 400 -l 50")
			s = print_program(best['prog'])
			GUI.show_formula(s)
			print("new best =", s)
		print("Gen%03d" % gen, end=' ')
		print("error =", round(best['fitness'],7))
	return best

def reinsert_best():
	if population[0] == best:
		print("Best candidate already in population")
	else:
		i = random.randint(0, len(population))
		population[i] = best
		print("Best candidate re-inserted into population")

import GUI

def main():
	# These allow the GUI module to access our constants and functions:
	GUI.search = search
	GUI.export_tree_as_graph = export_tree_as_graph
	GUI.print_program = print_program
	GUI.save_population = save_population
	GUI.load_population = load_population
	GUI.reinsert_best = reinsert_best

	GUI.max_gens = max_gens
	GUI.max_depth = max_depth
	GUI.pop_size = pop_size
	GUI.bouts = bouts
	GUI.p_repro = p_repro
	GUI.p_cross = p_cross
	GUI.p_mut = p_mut

	GUI.start_GUI()

print("Function Fitting by Genetic Programming\n")
main()
exit(0)
