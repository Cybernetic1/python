# -*- coding: utf-8 -*-

# Input: (x₁, x₂, ... , xₙ)
# output: (y₁, y₂, ... , yₙ)		(dimension of Y may be different from X's)

# Objective: Whenever X maps to Y, train all other permutations of X to map close to Y also
# Repeat with other random X's.

import numpy as np
from numpy.random import seed, rand

N = 2
L = 3

def layer_1_z(x, W):
	return np.insert(W, 1.0) * x

def layer_1_activation(x, W):
	z = layer_1_z(x, W)
	return np.sin(z)

# ==============================

def layer_2_z(x, W):
	return W * x + W[N + 1]

def layer_2_activation(x, W):
	z = layer_1_z(x, W)
	return np.sin(z)

# ==============================

def layer_3_z(x, W):
	return W * x + W[N + 1]

def layer_3_activation(x, W):
	z = layer_3_z(x, W)
	return np.sin(z)

# ==============================

def layer_2(x, W):
	y_hat = layer_1_activation(x, W)
	if y_hat > 0.5:
		return 1
	else:
		return 0

def loss(param):
	W = param
	x = rand(N) * 2.0 - 1.0 					# generate random x's from [-1,1]
	y_hat = layer_1_activation(x, W)
	error = np.square(layer_1_activation(x, W) - y_hat)
	return error

from sko.GA import GA

ga = GA(func = loss, n_dim = N + 1, size_pop = 50, max_iter = 100, lb = [-5, -5], ub = [5, 5], precision = 1e-5)
best_W, best_y = ga.run()
print('best_W:', best_W, '\n', 'best_y:', best_y)

# Testing:  (x₁ ... xₙ) --> (y₁ ... yₙ)
# Generate random x's from [-1,1].
# 
for x in range(100):
	y_hat = layer_2(x, best_W)
	print('输入数字{},是否是偶数:{}'.format(x, y_hat == 0))
