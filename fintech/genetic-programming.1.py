# -*- coding: utf8 -*-

# Experiments show the following:
# 1) for target X²+X+random(0,1), the learned function is Y = X/X = 1.0 or
#	Y = (-3.11X² - 3.33X - 2.53) / (X - 4.65) which looks hyperbolic / conic.
#	For target X²+X+random(0,10), the learned function is Y ≈ 0.5 which makes sense.
# 2) for target X²+random(0,1)X, a learned function is X²+0.5X which makes
#	sense also.
# 3) The best fitness can be surprisingly small due to random fluctuations.

import operator
import pygame
import math
import random

def rand_in_bounds(min, max):
	return random.uniform(min, max)

op_map = {
	operator.add : ' + ',
	operator.sub : ' - ',
	operator.mul : ' * ',
	operator.div : ' / ',
	}

def plot_population(screen, pop):
	H = 500
	h = float(H) - 4.0
	screen.fill((0x00,0x00,0x00))
	x = 0.0
	dx = 995.0 / len(pop)
	ymax = abs(pop[-1]['fitness'])
	ymax = 10.0
	for child in pop:
		y = int(child['fitness'] * h / ymax)
		if math.isnan(y):
			y = H - 3
		elif y > H - 3:
			y = H - 3
		elif y < -(H - 3):
			y = -(H - 3)
		x += dx
		# print y, ' ',
		c = 255.0 / (1.0 + math.exp(-0.002*float(child['len'])))
		pygame.draw.line(screen, (0xFF-int(c),0x00,0x00), [int(x),H], [int(x),H - y], 3)
	pygame.display.flip()

def print_program(node):
	if not isinstance(node, list):
		if isinstance(node, float):
			return str(round(node, 2))
		else:
			return node
	return "(" + print_program(node[1]) + op_map[node[0]] + print_program(node[2]) + ")"

def eval_program(node, dict):
	if not isinstance(node, list):
		if isinstance(node, float):
			return node
		if dict[node] is not None:
			return dict[node]
		return node
	arg1, arg2 = eval_program(node[1], dict), eval_program(node[2], dict)
	if node[0] == operator.div and arg2 == 0.0:
		return 0.0
	return apply(node[0], [arg1, arg2])

def generate_random_program(max, funcs, terms, depth = 0):
	if (depth == max - 1) or (depth > 1 and random.uniform(0.0,1.0) < 0.1):
		t = terms[random.randint(0, len(terms) - 1)]
		if t == 'R':
			return rand_in_bounds(-5.0, +5.0)
		else:
			return t
	depth += 1
	arg1 = generate_random_program(max, funcs, terms, depth)
	arg2 = generate_random_program(max, funcs, terms, depth)
	return [funcs[random.randint(0, len(funcs) - 1)], arg1, arg2]

def count_nodes(node):
	if not isinstance(node, list):
		return 1
	a1 = count_nodes(node[1])
	a2 = count_nodes(node[2])
	return a1 + a2 + 1

def target_function(x):
	return random.uniform(0.0, 10.0)
	return x**2 +random.uniform(0.0, 5.0)* x  + random.uniform(0.0,3.0)

def fitness(program, num_trials = 20):
	sum_error = 0.0
	for i in range(1, num_trials):
		x = rand_in_bounds(-1.0, 1.0)
		error = eval_program(program, {'X' : x}) - target_function(x)
		sum_error += abs(error)
	return sum_error / num_trials

def tournament_selection(pop, bouts):
	selected = []
	# print "bouts = ", bouts
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
	a2, cur_node = replace_node(node[2], replacement, node_num, cur_node)
	return [[node[0], a1, a2], cur_node]

def copy_program(node):
	# print node
	if not isinstance(node, list):
		return node
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
	a2, current_node = get_node(node[2], node_num, current_node)
	if a2:
		return a2, current_node
	return [], current_node

def prune(node, max_depth, terms, depth = 0):
	if depth == max_depth - 1:
		t = terms[random.randint(0, len(terms) - 1)]
		if t == 'R':
			return rand_in_bounds(-5.0, +5.0)
		else:
			return t
	depth += 1
	if not isinstance(node, list):
		return node
	a1 = prune(node[1], max_depth, terms, depth)
	a2 = prune(node[2], max_depth, terms, depth)
	return [node[0], a1, a2]

def crossover(parent1, parent2, max_depth, terms):
	pt1, pt2 = random.randint(1, count_nodes(parent1) - 1), \
		random.randint(1, count_nodes(parent2) - 1)
	# print "pt 1 & 2 = ", pt1, pt2
	tree1, c1 = get_node(parent1, pt1)
	tree2, c2 = get_node(parent2, pt2)
	# print "tree 1 & 2 = ", tree1, tree2
	child1, c1 = replace_node(parent1, copy_program(tree2), pt1)
	child1 = prune(child1, max_depth, terms)
	child2, c2 = replace_node(parent2, copy_program(tree1), pt2)
	child2 = prune(child2, max_depth, terms)
	return [child1, child2]

def mutation(parent, max_depth, functs, terms):
	random_tree = generate_random_program(max_depth / 2, functs, terms)
	point = random.randint(0, count_nodes(parent) - 1)
	child, count = replace_node(parent, random_tree, point)
	child = prune(child, max_depth, terms)
	return child

def search(max_gens, pop_size, max_depth, bouts, p_repro, p_cross, p_mut, functs, terms):
	population = []
	pygame.init()
	screen = pygame.display.set_mode((1000, 500))
	pygame.display.set_caption("Population fitness")
	raw_input("Press any key to start....")

	for i in range(0, pop_size):
		prog = generate_random_program(max_depth, functs, terms)
		population.append({'prog' : prog, \
			'fitness' : fitness(prog),
			'len' : count_nodes(prog)
			})
	best = sorted(population, key = lambda x : x['fitness'])[0]
	plot_population(screen, population)

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
				c1['prog'],c2['prog'] = crossover(p1['prog'], p2['prog'], max_depth, terms)
				children.append(c2)
			elif operation < p_repro + p_cross + p_mut:
				c1['prog'] = mutation(p1['prog'], max_depth, functs, terms)

		if len(children) < pop_size:
			children.append(c1)
		for c in children:
			c['fitness'] = fitness(c['prog'])
			c['len'] = count_nodes(c['prog'])
		population = children
		population = sorted(population, key = lambda x : x['fitness'])
		plot_population(screen, population)
		best['fitness'] = fitness(best['prog'])

		if population[0]['fitness'] <= best['fitness']:
			best = population[0]
		print "gen: ", gen,
		print "fitness = ", best['fitness']
		if best['fitness'] == 0.0:
			break
	return best

def main():
	# problem configuration
	terms = ['X', 'R']
	functs = [operator.add, operator.sub, operator.mul, operator.div]
	# algorithm configuration
	max_gens = 1000
	max_depth = 9
	pop_size = 100
	bouts = 5
	p_repro = 0.08
	p_cross = 0.90
	p_mut = 0.02
	# execute the algorithm
	best = search(max_gens, pop_size, max_depth, bouts, p_repro, p_cross, p_mut, functs, terms)
	print "Done!"
	print "best fitness = ", round(best['fitness'],4)
	# print best['prog']
	print "formula = ",
	print print_program(best['prog'])
	raw_input("Press any key to start....")

print("Genetic programming test")
main()
exit(0)
