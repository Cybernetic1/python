# -*- coding: utf8 -*-

import random
import operator
import math
import GUI

def rand_in_bounds(min, max):
	return random.uniform(min, max)

op_map = {
	operator.add : '+',
	operator.sub : '-',
	operator.mul : '*',
	operator.truediv : '÷',
	math.exp : 'e^',
	math.sqrt : '√',
	operator.pow : '^',
	}

# problem configuration
terms = ['x', 'y', 'R']

funcs = [
	operator.add,
	operator.sub,
	operator.mul,
	operator.truediv,
	math.exp,
	math.sqrt,
	operator.pow
	]

arity = {
	operator.add: 2,
	operator.sub: 2,
	operator.mul: 2,
	operator.truediv: 2,
	math.exp: 1,
	math.sqrt: 1,
	operator.pow: 2
	}

def print_program(node):
	if not isinstance(node, list):
		if isinstance(node, float):
			return str(round(node, 2))
		else:
			return node
	if arity[node[0]] == 1:
		return "(" + op_map[node[0]] + print_program(node[1]) + ")"
	return "(" + print_program(node[1]) + op_map[node[0]] + print_program(node[2]) + ")"

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
			return 0.0
	arg2 = eval_program(node[2], dict)
	if node[0] == operator.truediv and arg2 == 0.0:
		return 0.0
	try:
		return node[0](arg1, arg2)
	except:
		return 0.0

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

def fitness(program, num_trials = 10):
	# print("prog=", print_program(program))
	sum_error = 0.0
	for i in range(1, num_trials):
		x = rand_in_bounds(0.0, 2.0)
		# diagonal value:
		error = eval_program(program, {'x' : x, 'y' : x}) - 0.5
		sum_error += abs(error)
		# x- and y- axis value:
		z = 1.0 / (1.0 + math.exp(x)) - 0.5
		error = eval_program(program, {'x' : x, 'y' : 0.0}) - z
		sum_error += abs(error)
		error = eval_program(program, {'x' : 0.0, 'y' : x}) - z
		sum_error += abs(error)
	return sum_error / num_trials

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

def search(max_gens, pop_size, max_depth, bouts, p_repro, p_cross, p_mut):
	pygame.init()
	screen = pygame.display.set_mode((1000, 500))
	pygame.display.set_caption("Population fitness")

	population = []
	for i in range(0, pop_size):
		prog = generate_random_program(max_depth)
		population.append({'prog' : \
			prog, \
			'fitness' : \
			fitness(prog)})

	pop2 = sorted(population, key = lambda x : x['fitness'], reverse = False)
	best = pop2[0]
	plot_population(screen, pop2)
	input("Press any key to continue....")

	for gen in range(0, max_gens):
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

		if len(children) < pop_size:
			children.append(c1)
		for c in children:
			c['fitness'] = fitness(c['prog'])
		population = children
		population = sorted(population, key = lambda x : x['fitness'])

		plot_population(screen, population)
		quitting = False
		pausing = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitting = True
			elif event.type == pygame.KEYDOWN:
				pausing = True
			elif event.type == pygame.KEYUP:
				pausing = False
		while pausing:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quitting = True
					pausing = False
				elif event.type == pygame.KEYUP:
					pausing = False

		if population[0]['fitness'] <= best['fitness']:
			best = population[0]
		print("gen", gen, end=' ')
		print("fitness =", best['fitness'])
		if best['fitness'] == 0:
			break
	return best

def main():
	# algorithm configuration
	max_gens = 3000
	max_depth = 6
	pop_size = 200
	bouts = 5
	p_repro = 0.08
	p_cross = 0.80
	p_mut = 0.02
	# execute the algorithm
	GUI.start_GUI(max_gens, max_depth, pop_size, bouts, p_repro, p_cross, p_mut)
	best = search(max_gens, pop_size, max_depth, bouts, p_repro, p_cross, p_mut)
	print("Done!")
	print("best fitness = ", round(best['fitness'],4))
	# print(best['prog'])
	print("formula = ", end='\t')
	print(print_program(best['prog']))

print("Genetic programming test")
main()
exit(0)
