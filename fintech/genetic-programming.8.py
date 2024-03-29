# -*- coding: utf8 -*-

# This is the last version that learns to buy/sell.
# Next version will focus on next-day price prediction, which I think is
# a simpler and more effective strategy.

# Explanation:
# Goal of learning is to learn 2 functions:
# (1) the boolean condition C of whether to place a limit order or not
# (2) the real function T of the target price of the limit order
# C and T are dependent on 20 real-number variables

# TO-DO:
# * create pool of auxiliary variables
# * Ko's new fitness
# * 一交配就产生不良孩子
# * first question is why does random generation seem so good?
# * why does cross-over generate worse children?
# * 

import random
import operator
import sys
import math
import pygame

cache = []		# for storing previously-learned best formulas

opens = []
highs = []
lows = []
closes = []

'''
// **** Convert dates to DD/MM/YY format
f = open("dates.txt", "w")
with open("ES_OHLC.txt") as datafile:
	for line in datafile:
		nums = line[:-3].split(',')
		if nums[0][0] == '1':
			dd = nums[0][5:7]
			mm = nums[0][3:5]
			yy = nums[0][1:3]
		else:
			dd = nums[0][4:6]
			mm = nums[0][2:4]
			yy = nums[0][0:2]
		f.write(dd + '-' + mm + '-' + yy + '\n')
exit(0)
'''

print "Reading OHLC data...."
with open("ES_OHLC.txt") as datafile:
	for line in datafile:
		nums = line[:-3].split(',')		# get rid of ';' at end of line
		opens.append(float(nums[1]))
		highs.append(float(nums[2]))
		lows.append(float(nums[3]))
		closes.append(float(nums[4]))

e20s = []			# 20-day moving average (exponential)
e100s = []			# 100-day moving average (exponential)
avgs = []			# 100-day average daily range

datasize = len(opens)
print "Data size = ", datasize

print "Calculating moving averages and average daily range...."
k20 = 2 / 21
k100 = 2 / 101
sum0 = 0
sum20 = 0
sum100 = 0
for i in range(0, datasize):
	# calculate avarage daily range
	daily_range = highs[i] - lows[i]
	sum0 += daily_range
	avgs.append(sum0 / (100 if i > 99 else i + 1))

	# calculate 20-day EMA
	if (i < 20):		# for i = 0...19 = first 20 days
		sum20 += closes[i]
		e20s.append(sum20 / (i + 1))
	else:
		e20s.append(closes[i] * k20 + (1 - k20) * e20s[i - 1])

	# calculate 100-day EMA
	if (i < 100):		# for i = 0...99 = first 100 days
		sum100 += closes[i]
		e100s.append(sum100 / (i + 1))
	else:
		e100s.append(closes[i] * k100 + (1 - k100) * e100s[i - 1])

def plot_population(screen, pop):
	screen.fill((0x00,0x00,0x00))
	x = 1.0
	dx = 999.0 / len(pop)
	# dn = int(math.ceil(dx))
	dn = int(dx)
	ymax = abs(pop[-1]['fitness'])
	for child in pop:
		z = child['fitness']
		x += dx
		if z >= 0.0:
			pygame.draw.line(screen, (0xFF,0x00,0x00), [int(x),250], [int(x),250-int(z*10.0)], dn)
		else:
			y = int(z * 245.0 / ymax)
			pygame.draw.line(screen, (0x00,0x00,0xFF), [int(x),250], [int(x),250-y], dn)
	pygame.display.flip()

def plot_OHLC():
	from numpy import * 		# used in plotting
	import plotly.plotly as py	# communicate with external plotly server
	import plotly.graph_objs as go

	N = 100     # Number of boxes

	# Each box is represented by a dict that contains the data, the type, and the colour. 
	# Use list comprehension to describe N boxes
	data = [{
		'y': [opens[i], highs[i], lows[i], closes[i]],
		'type':'box',
		'marker':{'color': 'green'}
		} for i in range(int(N))]

	# format the layout
	layout = {'xaxis': {'showgrid':False,'zeroline':False, 'tickangle':60,'showticklabels':False},
			  'yaxis': {'zeroline':False,'gridcolor':'white'},
			  'paper_bgcolor': 'rgb(233,233,233)',
			  'plot_bgcolor': 'rgb(233,233,233)',
			  'showlegend':False}

	url = py.plot(data,layout=layout,filename='Box plot')

def plot_EMAs():
	# from numpy import * 		# used in plotting
	import plotly.plotly as py	# communicate with external plotly server
	import plotly.graph_objs as go

	N = 100     # Number of boxes

	# Each box is represented by a dict that contains the data, the type, and the colour. 
	# Use list comprehension to describe N boxes
	data = [{
		'y': [opens[i], highs[i], lows[i], closes[i]],
		'type':'box',
		'marker':{'color': 'green'}
		} for i in range(int(N))]

	# format the layout
	layout = {'xaxis': {'showgrid':False,'zeroline':False, 'tickangle':60,'showticklabels':False},
			  'yaxis': {'zeroline':False,'gridcolor':'white'},
			  'paper_bgcolor': 'rgb(233,233,233)',
			  'plot_bgcolor': 'rgb(233,233,233)',
			  'showlegend':False}

	url = py.plot(data,layout=layout,filename='Box plot')

# Global variables

max_gens = 50
max_depth = 7	# 7
pop_size = 100	# 100
bouts = 5
p_repro = 0.08	# 0.08
p_cross = 0.90	# 0.90
p_mut = 0.02	# 0.02

def rand_in_bounds(min, max):
	return random.uniform(min, max)

op_map = {
	operator.add : ' + ',
	operator.sub : ' - ',
	operator.mul : ' * ',
	operator.div : ' ÷ ',

	operator.and_ : ' ∧ ',
	operator.or_ : ' ∨ ',
	operator.gt : ' > ',
	operator.lt : ' < ',
	}

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
	f.write("node" + str(index) + "[label=\"" + op_map[node[0]] + color)
	f.write("node" + str(index) + " -> node" + str(index + 1) + ";\n")
	count1 = print_tree_as_graph(f, node[1], index + 1)
	f.write("node" + str(index) + " -> node" + str(index + count1 + 1) + ";\n")
	count2 = print_tree_as_graph(f, node[2], index + count1 + 1)
	return count1 + count2 + 1

def print_tree(node, tabs = ""):
	if not isinstance(node, list):
		if isinstance(node, float):
			return str(round(node, 2))
		else:
			return node
	return tabs + op_map[node[0]] + "\n" + \
		tabs + print_tree(node[1], tabs + "    ") + "\n" + \
		tabs + print_tree(node[2], tabs + "    ")

def read_tree(str):			# assume str is in prefix notation with ()'s
	if str[0] == '(':
		op = str[1]
		return [
			op,
			read_tree(str[2:]),
			read_tree(str),
			]
	return None

def eval_tree(node, time):
	if not isinstance(node, list):
		if isinstance(node, float):
			return node
		# elif dict[node] is not None:
		elif node == 'O1':
			return opens[time - 1]
		elif node == 'H1':
			return highs[time - 1]
		elif node == 'L1':
			return lows[time - 1]
		elif node == 'C1':
			return closes[time - 1]

		elif node == 'O2':
			return opens[time - 2]
		elif node == 'H2':
			return highs[time - 2]
		elif node == 'L2':
			return lows[time - 2]
		elif node == 'C2':
			return closes[time - 2]

		elif node == 'O3':
			return opens[time - 3]
		elif node == 'H3':
			return highs[time - 3]
		elif node == 'L3':
			return lows[time - 3]
		elif node == 'C3':
			return closes[time - 3]

		elif node == 'O4':
			return opens[time - 4]
		elif node == 'H4':
			return highs[time - 4]
		elif node == 'L4':
			return lows[time - 4]
		elif node == 'C4':
			return closes[time - 4]

		elif node == 'Ot':
			return opens[time]
		elif node == 'E20':
			return e20s[time - 1]
		elif node == 'E100':
			return e100s[time - 1]
		elif node == 'Avg':
			return avgs[time - 1]

		else:
			return node
	arg1 = eval_tree(node[1], time)
	arg2 = eval_tree(node[2], time)
	if node[0] == operator.div and arg2 == 0.0:
		return float('nan')
	return apply(node[0], [arg1, arg2])

def generate_random_formula(max, funcs, terms, depth = 0):
	if (depth == max - 1) or (depth > 1 and random.uniform(0.0,1.0) < 0.1):
		t = terms[random.randint(0, len(terms) - 1)]
		if t == 'R':
			return rand_in_bounds(-5.0, +5.0)
		else:
			return t
	depth += 1
	arg1 = generate_random_formula(max, funcs, terms, depth)
	arg2 = generate_random_formula(max, funcs, terms, depth)
	return [funcs[random.randint(0, len(funcs) - 1)], arg1, arg2]

# Needs to generate a random condition in 3 stages:
# 1) ∧ and ∨
# 2) > and <
# 3) formula
def generate_random_condition(max, funcs, terms, depth = 0):
	if (depth == max - 1) or (depth > 1 and random.uniform(0.0,1.0) < 0.1):
		return generate_random_inequality(max - depth, funcs, terms)
	depth += 1
	arg1 = generate_random_condition(max, funcs, terms, depth)
	arg2 = generate_random_condition(max, funcs, terms, depth)
	op = operator.and_ if (random.uniform(0.0, 1.0) > 0.5) else operator.or_
	return [op, arg1, arg2]

def generate_random_inequality(max, funcs, terms):
	# determine max = ?
	arg1 = generate_random_formula(max, funcs, terms)
	arg2 = generate_random_formula(max, funcs, terms)
	op = operator.gt if (random.uniform(0.0, 1.0) > 0.5) else operator.lt
	return [op, arg1, arg2]

def count_nodes(node):
	if not isinstance(node, list):
		return 1
	a1 = count_nodes(node[1])
	a2 = count_nodes(node[2])
	return a1 + a2 + 1

# ***** Calculate profit.
# On each day, a limit order (either long or short) will be placed at price T.
# If T > opening price O(t) on that day, T will be a long order, otherwise short.
# For a long order, if the high price H(t) > T, the order will be triggered.
# The profit is then O(t) - T.
# If the order is not triggered, the profit / loss would depend on the closing
# price C(t).  The profit (or loss) would be C(t) - E(t) = C(t) - O(t).

def fitness(formula, cond = None, num_trials = 200):
	sum_profit = 0.0
	for i in range(0, num_trials):
		time = random.randint(100, datasize - 10)
		target = eval_tree(formula, time)
		# print "target = ", target
		# print "Condition = ", print_tree(cond)
		# c = eval_tree(cond, time)
		# if not c:
		#	continue
		if target < 0.0:
			sum_profit -= 50.0
			continue
		if target > 10000.0:
			sum_profit -= 50.0
			continue
		if math.isnan(target):
			sum_profit -= 1000.0
			continue
		if highs[time] > target:
			if target > opens[time]:
				sum_profit += (target - opens[time])
		else:
			sum_profit += (closes[time] - opens[time])
		# print "Condition satisfied"
		# print "profit = ", sum_profit
		# sum_profit += profit
	return sum_profit / num_trials

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

def copy_tree(node):
	# print node
	if not isinstance(node, list):
		return node
	return [node[0], copy_tree(node[1]), copy_tree(node[2])]

def get_node(node, node_num, current_node = 0):
	if current_node == node_num:
		return node, (current_node + 1)
	current_node += 1
	if not isinstance(node, list):		# is a var or number
		return [], current_node
	a1, current_node = get_node(node[1], node_num, current_node)
	if a1:		# a1 != []
		return a1, current_node
	a2, current_node = get_node(node[2], node_num, current_node)
	if a2:		# a2 != []
		return a2, current_node
	return [], current_node		# ?? will we ever get here?

# TO-DO:  prune needs to respect boolean structure
def prune(node, max_depth, terms, depth = 0):
	depth += 1
	if not isinstance(node, list):
		return node
	if is_arith(node):
		a1 = prune2(node[1], max_depth, terms, depth)
		a2 = prune2(node[2], max_depth, terms, depth)
		return [node[0], a1, a2]
	else:
		a1 = prune(node[1], max_depth, terms, depth)
		a2 = prune(node[2], max_depth, terms, depth)
		return [node[0], a1, a2]

def prune2(node, max_depth, terms, depth = 0):
	if depth >= max_depth - 1:
		t = terms[random.randint(0, len(terms) - 1)]
		if t == 'R':
			return rand_in_bounds(-5.0, +5.0)
		else:
			return t
	depth += 1
	if not isinstance(node, list):
		return node
	a1 = prune2(node[1], max_depth, terms, depth)
	a2 = prune2(node[2], max_depth, terms, depth)
	return [node[0], a1, a2]

def crossover(parent1, parent2, max_depth, terms):
	pt1 = random.randint(1, count_nodes(parent1) - 1)
	pt2 = random.randint(1, count_nodes(parent2) - 1)
	# print "pt 1 & 2 = ", pt1, pt2
	# c1, c2 are dummy variables
	tree1, c1 = get_node(parent1, pt1)
	tree2, c2 = get_node(parent2, pt2)
	# print "tree 1 & 2 = ", tree1, tree2
	child1, c1 = replace_node(parent1, copy_tree(tree2), pt1)
	child1 = prune(child1, max_depth, terms)
	child2, c2 = replace_node(parent2, copy_tree(tree1), pt2)
	child2 = prune(child2, max_depth, terms)
	return [child1, child2]

# crossover for conditions
def crossover_cond(parent1, parent2, max_depth, terms):
	if random.uniform(0.0, 1.0) > 0.5:
		return crossover_cond1(parent1, parent2, max_depth, terms)
	else:
		return crossover_cond2(parent1, parent2, max_depth, terms)

def is_boolean(node):
	if not isinstance(node, list):
		return False
	else:
		op = node[0]
		return (op == operator.and_) or (op == operator.or_)

# randomly cross at boolean layer (choose 2 points in boolean layers)
def crossover_cond1(parent1, parent2, max_depth, terms):
	# print "Crossing boolean layer"
	while True:
		pt1 = random.randint(1, count_nodes(parent1) - 1)
		tree1, c = get_node(parent1, pt1)
		if is_boolean(tree1):		# test if tree is boolean
			break

	while True:
		pt2 = random.randint(1, count_nodes(parent2) - 1)
		tree2, c = get_node(parent2, pt2)
		if is_boolean(tree2):		# test if tree is boolean
			break

	# print "tree 1 & 2 = ", tree1, tree2
	child1, c = replace_node(parent1, copy_tree(tree2), pt1)
	child1 = prune(child1, max_depth, terms)
	child2, c = replace_node(parent2, copy_tree(tree1), pt2)
	child2 = prune(child2, max_depth, terms)
	return [child1, child2]

def is_arith(node):
	if not isinstance(node, list):
		return True
	else:
		op = node[0]
		return \
		(op == operator.add) or \
		(op == operator.sub) or \
		(op == operator.mul) or \
		(op == operator.div)

# randomly cross some inequalities? (choose 2 points in inequalities)
def crossover_cond2(parent1, parent2, max_depth, terms):
	# print "Crossing arithmetic layer"
	while True:
		pt1 = random.randint(1, count_nodes(parent1) - 1)
		tree1, c = get_node(parent1, pt1)
		if is_arith(tree1):		# test if tree is arithmetic
			break

	while True:
		pt2 = random.randint(1, count_nodes(parent2) - 1)
		tree2, c = get_node(parent2, pt2)
		if is_arith(tree2):		# test if tree is arithmetic
			break

	# print "tree 1 & 2 = ", tree1, tree2
	child1, c = replace_node(parent1, copy_tree(tree2), pt1)
	child1 = prune(child1, max_depth, terms)
	child2, c = replace_node(parent2, copy_tree(tree1), pt2)
	child2 = prune(child2, max_depth, terms)
	return [child1, child2]

def mutation(parent, max_depth, funcs, terms):
	point = random.randint(0, count_nodes(parent) - 1)
	random_tree = generate_random_formula(max_depth / 2, funcs, terms)
	child, count = replace_node(parent, random_tree, point)
	child = prune(child, max_depth, terms)
	return child

def mutation_cond(parent, max_depth, funcs, terms):
	point = random.randint(0, count_nodes(parent) - 1)
	# need to determine type of "replacement"
	tree, c = get_node(parent, point)
	if is_arith(tree):
		random_tree = generate_random_formula(max_depth / 2, funcs, terms)
	elif is_boolean(tree):
		random_tree = generate_random_condition(max_depth / 2, funcs, terms)
	else:
		random_tree = generate_random_formula(max_depth / 2, funcs, terms)
		if random.uniform(0.0, 1.0) > 0.5:
			point += 1		# node number of left child
		else:
			point += count_nodes(tree[1])	# node number of right child

	child, count = replace_node(parent, random_tree, point)
	child = prune(child, max_depth, terms)
	return child

# problem configuration

terms = [
		# 'O1', 'H1', 'L1', 'C1',
		# 'O2', 'H2', 'L2', 'C2',
		# 'O3', 'H3', 'L3', 'C3',
		# 'O4', 'H4', 'L4', 'C4',
		'Ot',				# today's open price
		'E20',				# 20-day moving average (exponential)
		'E100',				# 100-day moving average (exponential)
		'Avg',				# 100-day average daily range
		'R']			# 'R' invokes random number generator

arith_ops = [
	operator.add,
	operator.sub,
	operator.mul,
	operator.div
	]

def search():
	global max_gens, pop_size, max_depth, bouts, p_repro, p_cross, p_mut
	population = []

	pygame.init()
	screen = pygame.display.set_mode((1000, 500))
	pygame.display.set_caption("Population fitness")

	print "Generating population..."
	for c in cache:
		population.append({
			'target' : c['target'],
			'fitness' : fitness(c['target'])
		})
	print "Adding from cache:", len(cache)
	for i in range(0, pop_size - len(cache)):
		print i, ' ',
		sys.stdout.flush()
		# print "\tGenerating formula..."
		target = generate_random_formula(max_depth, arith_ops, terms)
		# print "\tGenerating condition..."
		# cond = generate_random_condition(max_depth, arith_ops, terms)
		population.append({
			'target' : target, \
			# 'cond' : cond, \
			'fitness' : fitness(target)})
	print
	pop2 = sorted(population, key = lambda x : x['fitness'], reverse = True)
	best = pop2[0]
	plot_population(screen, pop2)
	raw_input("Press any key to continue....")

	for gen in range(0, max_gens):
		children = []
		# print "\nGenerating children..."
		while len(children) < pop_size:
			operation = random.uniform(0.0, 1.0)
			p1 = tournament_selection(population, bouts)
			c1 = {}
			if operation < p_repro:
				c1['target'] = copy_tree(p1['target'])
				# c1['cond'] = copy_tree(p1['cond'])
			elif operation < p_repro + p_cross:
				p2 = tournament_selection(population, bouts)
				c2 = {}
				c1['target'],c2['target'] = crossover(p1['target'], p2['target'], max_depth, terms)
				# c1['cond'],  c2['cond']   = crossover_cond(p1['cond'],   p2['cond'],   max_depth, terms)
				# print "***** crossed condition = ", print_tree(c1['cond'])
				children.append(c2)
			elif operation < p_repro + p_cross + p_mut:
				c1['target'] = mutation(p1['target'], max_depth, arith_ops, terms)
				# c1['cond']   = mutation_cond(p1['cond'],   max_depth, arith_ops, terms)
				# print "***** mutated condition = ", print_tree(c1['cond'])
			if len(children) < pop_size:
				children.append(c1)

		# print "Evaluating children..."
		for c in children:
			# print "c's Condition = ", print_tree(c['cond'])
			c['fitness'] = fitness(c['target'])
		best['fitness'] = fitness(best['target'], None, 500)
		# population = children
		population = sorted(children, key = lambda x : x['fitness'], reverse = True)
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

		print "[", gen, "]",
		print "best in pop =", round(population[0]['fitness'],2), "\tprevious best =", round(best['fitness'],2)
		if population[0]['fitness'] >= best['fitness']:
			best = population[0]
		else:
			population = [best] + population[:-1]
		# if best['fitness'] == 0:
		#	break
	return best

import Tkinter as tk
root = tk.Tk()
root.title("Genetic programming test")
best = {}

def butt_train_pop():
	global max_gens, pop_size, max_depth, bouts, p_repro, p_cross, p_mut
	global best
	max_gens  = int(text1.get("1.0", tk.END)[:-1])
	pop_size  = int(text1c.get("1.0", tk.END)[:-1])
	max_depth = int(text1b.get("1.0", tk.END)[:-1])
	bouts     = int(text1a.get("1.0", tk.END)[:-1])
	p_repro   = float(text0c.get("1.0", tk.END)[:-1])
	p_cross   = float(text0b.get("1.0", tk.END)[:-1])
	p_mut     = float(text0a.get("1.0", tk.END)[:-1])

	# execute the algorithm
	best = search()
	print "Done!"
	print "best fitness = ", round(best['fitness'],4)
	from subprocess import call
	call(["beep"])

def butt_export_graph():
	s = text2.get("1.0", tk.END)
	if s == "\n":
		fname = "formula.dot"
	else:
		fname = s[:-1]
	print "Exporting best formula as graph...."
	export_tree_as_graph(best['target'], fname)
	from subprocess import call
	call(["dot", "-Tpng", "-O", fname])
	call(["eog", fname + ".png"])

def butt_print_best():
	# print "condition = "
	# print print_tree(best['cond'])
	print "target = "
	print print_tree(best['target'])

def butt_verify_best():
	sum_fitness = 0.0
	sum_squares = 0.0
	num_tests = 100
	for i in range(0, num_tests):
		time = random.randint(100, datasize - 10)
		target = eval_tree(best['target'], time)
		profit = fitness(best['target'])
		print "[", time, "]", round(target,2), round(profit,2)
		sum_fitness += profit
		sum_squares += (profit * profit)
	print "total profit =", round(sum_fitness,2)
	avg = sum_fitness / num_tests
	print "average profit per day =", round(avg,2)
	print "variance =", math.sqrt(sum_squares / num_tests - avg * avg)

def butt_verify_best_full():
	sum_fitness = 0.0
	sum_squares = 0.0
	N = float(datasize - 110) / 100.0
	for i in range(0, datasize - 110):
		print round(i / N, 0), "%\r",
		time = i + 100
		# target = eval_tree(best['target'], time)
		profit = fitness(best['target'])
		# print "[", time, "]", round(target,2), round(profit,2)
		sum_fitness += profit
		sum_squares += (profit * profit)
	print "total profit =", sum_fitness
	N = float(datasize - 110)
	print "N =", N
	avg = sum_fitness / N
	print "average profit =", avg
	print "variance =", math.sqrt(sum_squares / N - avg * avg)

def butt_export_Excel():
	print "Saving to Excel...."
	s = textC.get("1.0", tk.END)
	if s == "\n":
		f = open("results.csv", 'w')
	else:
		f = open(s[:-1], 'w')
	N = float(datasize - 110) / 100.0
	for i in range(0, datasize - 110):
		print round(i / N, 0), "%\r",
		sys.stdout.flush()
		time = i + 100
		target = eval_tree(best['target'], time)
		profit = fitness(best['target'])
		f.write(str(round(target,2)) + ",")
		f.write(str(round(profit,2)) + "\n")
	print
	# f.write("\n")
	f.close()

def butt_save_best():
	s = text8.get("1.0", tk.END)
	if s == "\n":
		f = open("formula", 'wb')
	else:
		f = open(s[:-1], 'wb')
	import pickle
	pickle.dump(best, f, pickle.HIGHEST_PROTOCOL)
	f.close()
	print "Formula saved"

def butt_load_best():
	s = text7.get("1.0", tk.END)
	if s == "\n":
		f = open("formula", 'rb')
	else:
		f = open(s[:-1], 'rb')
	import pickle
	best = pickle.load(f)
	f.close()
	cache.append(best)
	print "Formula loaded into cache"

def butt_input_best():
	s = text9.get("1.0", tk.END)
	s2 = s[:-1]
	s = s2.replace("+", "operator.add")
	s2 = s.replace("-", "operator.sub")
	s = s2.replace("*", "operator.mul")
	s2 = s.replace("/", "operator.div")
	target = eval(s2)
	print target
	best = {
		'target' : target,
		'fitness' : fitness(target, None, 500)
		}		
	cache.append(best)
	print "Formula read into cache, current cache size =", len(cache)
	msgA.config(text = "cache size = " + str(len(cache)))

def butt_write_best():
	s = text8.get("1.0", tk.END)
	if s == "\n":
		import glob #, os
		# os.chdir("~/fintech")
		maxnum = 0
		suffix = ""
		for fname in glob.glob("f[0-9]*"):
			s = fname.split('.')
			num = int(s[0][1:])
			if num > maxnum:
				maxnum = num
				if len(s) == 2: suffix = s[1]
		fname = "f" + str(maxnum + 1)
	else:
		fname = s[:-1]
	f = open(fname, 'w')
	print >> f, best['target']
	f.close()
	print "Formula written to:", fname

def butt_read_best():
	s = text7.get("1.0", tk.END)
	if s == "\n":
		import glob #, os
		# os.chdir("~/fintech")
		maxnum = 0
		suffix = ""
		for fname in glob.glob("f[0-9]*"):
			s = fname.split('.')
			print s
			num = int(s[0][1:])
			if num > maxnum:
				maxnum = num
				if len(s) == 2: suffix = s[1]
		fname = "f" + str(maxnum) + ('' if suffix == "" else '.' + suffix)
	else:
		import glob
		matches = glob.glob(s[:-1] + "*")
		if matches == []:
			fname = s[:-1]
		else:
			fname = matches[0]
	f = open(fname, 'r')
	s = f.read()
	f.close()
	s2 = s.replace("<built-in function add>", "operator.add")
	s = s2.replace("<built-in function sub>", "operator.sub")
	s2 = s.replace("<built-in function mul>", "operator.mul")
	s = s2.replace("<built-in function div>", "operator.div")
	target = eval(s)
	# print target
	global best
	best = {
		'target' : target,
		'fitness' : fitness(target, None, 500)
		}
	cache.append(best)
	print "Formula read into cache, current cache size =", len(cache)
	msgA.config(text = "cache size = " + str(len(cache)))

def butt_clear_cache():
	cache = []
	print "Cache cleared"
	msgA.config(text = "cache size = " + str(len(cache)))

# [s] save best formula\n\
# [l] load best formula\n\
tk.Label(root, text="P(cross)").grid(row=0, column=0, sticky=tk.W)
text0b = tk.Text(root, height=1, width=10)
text0b.grid(row=0,column=0)
text0b.insert(tk.END, str(p_cross))
tk.Label(root, text="P(mutate)").grid(row=0, column=1, sticky=tk.W)
text0a = tk.Text(root, height=1, width=10)
text0a.grid(row=0,column=1,sticky=tk.E)
text0a.insert(tk.END, str(p_mut))
tk.Label(root, text="P(repro)").grid(row=0, column=2, sticky=tk.W)
text0c = tk.Text(root, height=1, width=10)
text0c.grid(row=0,column=2,sticky=tk.E)
text0c.insert(tk.END, str(p_repro))

button2 = tk.Button(root, text="Train population", command=butt_train_pop)
button2.grid(row=2,column=0)
tk.Label(root, text="#Gens").grid(row=2, column=1, sticky=tk.W)
text1 = tk.Text(root, height=1, width=10)
text1.grid(row=2,column=1,sticky=tk.E)
text1.insert(tk.END, str(max_gens))
tk.Label(root, text="bouts").grid(row=1, column=2, sticky=tk.W)
text1a = tk.Text(root, height=1, width=10)
text1a.grid(row=1,column=2,sticky=tk.E)
text1a.insert(tk.END, str(bouts))
tk.Label(root, text="depth").grid(row=2, column=2, sticky=tk.W)
text1b = tk.Text(root, height=1, width=10)
text1b.grid(row=2,column=2,sticky=tk.E)
text1b.insert(tk.END, str(max_depth))
tk.Label(root, text="pop size").grid(row=1, column=1, sticky=tk.W)
text1c = tk.Text(root, height=1, width=10)
text1c.grid(row=1,column=1,sticky=tk.E)
text1c.insert(tk.END, str(pop_size))

button3 = tk.Button(root, text="export best formula as graph", command=butt_export_graph)
button3.grid(row=3,column=0)
text2 = tk.Text(root, height=1, width=50)
text2.grid(row=3,column=1,columnspan=2)
text2.insert(tk.END, "formula.dot")
button4 = tk.Button(root, text="print best formula", command=butt_print_best)
button4.grid(row=4,column=0)
button5 = tk.Button(root, text="verify best formula", command=butt_verify_best)
button5.grid(row=5,column=0)
button6 = tk.Button(root, text="verify best formula with full history", command=butt_verify_best_full)
button6.grid(row=6,column=0)
button7 = tk.Button(root, text="read best formula", command=butt_read_best)
button7.grid(row=7,column=0)
text7 = tk.Text(root, height=1, width=50)
text7.grid(row=7,column=1,columnspan=2)
# text7.insert(tk.END, "f1")
button8 = tk.Button(root, text="write best formula", command=butt_write_best)
button8.grid(row=8,column=0)
text8 = tk.Text(root, height=1, width=50)
text8.grid(row=8,column=1,columnspan=2)
# text8.insert(tk.END, "f1")
button9 = tk.Button(root, text="input best formula in Lisp format", command=butt_input_best)
button9.grid(row=9,column=0)
text9 = tk.Text(root, height=1, width=50)
text9.grid(row=9,column=1,columnspan=2)
text9.insert(tk.END, "(+ 1 2)")
buttonA = tk.Button(root, text="clear formula cache", command=butt_clear_cache)
buttonA.grid(row=10,column=0)
msgA = tk.Message(root, width=100, text="cache size = " + str(len(cache)))
msgA.grid(row=10,column=1)
buttonC = tk.Button(root, text="save as Excel", command=butt_export_Excel)
buttonC.grid(row=12,column=0)
textC = tk.Text(root, height=1, width=50)
textC.grid(row=12,column=1,columnspan=2)
textC.insert(tk.END, "results.csv")
# buttonD = tk.Button(root, text="quit", command=exit)
# buttonD.grid(row=1,column=0)
buttonD = tk.Button(root, text="Plot OHLC", command=plot_OHLC)
buttonD.grid(row=13,column=0)
msg = tk.Message(root, width=800, text="(C) LK Lam, YKY 2015")
msg.grid(row=14,column=0,columnspan=3)

root.mainloop()
exit(0)
