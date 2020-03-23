import numpy
from math import factorial, isnan
from itertools import permutations
import time
numpy.random.seed(int(time.time()))

N = 2			# dimension of input X

def sigmoid(x):
	return 1.0 / (1.0 + numpy.exp(-3.0 * x))

def relu(x):
	result = x
	result[x<0] = 0
	return x

def set_distance(x1, x2):
	Σ = 0.0
	for i in range(N):
		for j in range(N):
			Σ += numpy.abs(x1[i] - x2[j]) * 2 \
			   - numpy.abs(x1[i] - x1[j]) \
			   - numpy.abs(x2[i] - x2[j])
	dx = Σ / (N**2)
	if dx < -1e-10:
		print("x1=", x1)
		print("x2=", x2)
		print("Σ1=", Σ1)
		print("Σ2=", Σ2)
		print("Σ3=", Σ3)
		print("dx=", dx)
		raise ValueError("distance < 0")
	# else:
		# print("dx=", dx)
		# print(".", end='')
	return dx

def distance(y1, y2):
	Σ = 0.0
	for i in range(N):
		Σ += (y1[i] - y2[i])**2
	return numpy.sqrt(Σ)

# ***** Old functions, no longer useful *****

def threshold1(r):
	return 1.0 / (numpy.exp(1.0 - r)) - 1.0

def threshold2(y):
	ɛ = 0.005
	Ʊ = 1e10
	δ = 0.01
	Ω = 10.0
	if y < ɛ:
		return (Ʊ / ɛ)* y + Ʊ
	else:
		return (-δ / Ω)* y + δ
	"""
	return 1e-6 / (numpy.exp(y) - 1.0)
	"""

# ***** This miraculously good-looking function was found by serendipity
def joint_penalty(x, y):
	k = 1.0			# "Steepness"
	return numpy.exp(-k * (x**2 + y**2)) - numpy.exp(-2.0 * k * x * y)

def perturb(x):
	if numpy.random.randint(2) > 0:
		# apply random permutation
		return numpy.random.permutation(x)
	else:
		# generate random new value
		return numpy.random.rand(N) * 2.0 - 1.0

def predict_outputs(weights_mat, activation="ReLU"):
	# generate random X, find all permutions, variance should tend to zero
	penalties = 0.0
	x0 = numpy.random.rand(N) * 2.0 - 1.0
	y0 = x0
	for curr_weights in weights_mat:		# for each layer
		y0 = numpy.matmul(y0, curr_weights)
		if activation == "ReLU":
			y0 = relu(y0)
		elif activation == "sigmoid":
			y0 = sigmoid(y0)
	x = x0
	y = y0
	for i in range(100):
		x0 = x
		y0 = y
		x = perturb(x0)
		# print("x=", x)
		# print("x0=", x0)
		y = x
		for curr_weights in weights_mat:		# for each layer
			y = numpy.matmul(y, curr_weights)
			if activation == "ReLU":
				y = relu(y)
			elif activation == "sigmoid":
				y = sigmoid(y)
		dx = set_distance(x, x0)
		dy = distance(y, y0)
		penalty = joint_penalty(dy, dx)
		# print("dx=", dx)
		# print("y=", y)
		# print("y0=", y0)
		# print("dy=", dy)
		# print("penalty=", penalty)
		penalties += penalty
	return penalties

def fitness(weights_mat, activation="ReLU"):
	accuracy = numpy.empty(shape=(weights_mat.shape[0]))
	for soln_idx in range(weights_mat.shape[0]):
		curr_soln_mat = weights_mat[soln_idx, :]
		accuracy[soln_idx] = predict_outputs(curr_soln_mat, activation=activation)
	return accuracy
