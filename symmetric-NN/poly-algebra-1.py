# Polynomial algebra -- programmatically compute invariant weight colors
# ======================================================================

# TO-DO:
# * 

# The program (this version) computes the output for 1 layer:
# 1. Each output component is a polynomial given by the single-layer equation,
#		of the form: A x^E where A = coefficient, E = exponent
# 2. Single-layer equation:
#		yₖ = Wₖ x x + Wₖ x + Wₖ
# 3. The exponent E can be implemented as a list E = [e₁, ..., eₙ]
#		each eⱼ denotes exponent of j-th variable xⱼ
# 4. Each coefficient A may be an (integral) polynomial in terms of the weights Wᵢⱼₖₗ.
#		On the 1st layer, every A is just a single W.
#		But at this point, I don't know what happens when layers are composed.
#		Let's see... 1 layer consists of all possible terms of degree ≤ 2, in the sense that
#		each yᵢ is the 'free' deg-2 polynomial.
#		The 2nd layer would consist of the free polynomial of deg 4?  That seems incorrect...
#		Because the 1st-layer output is just n free deg-2 polynomials.

import numpy as np

def subscript(i):
	return "₀₁₂₃₄₅₆₇₈₉"[i]

def superscript(i):
	return "⁰¹²³⁴⁵⁶⁷⁸⁹"[i]

# We need a representation of polynomials in the weights Wᵢⱼₖₗ
# but we may also need a representation of polynomials in the variables Xₗₖ
# the coefficients of the latter are polynomials.

class Poly_in_X:
	# A polynomial is just a sum of monomials
	def __init__(self, *monos):
		self.monos = monos

	# **** Adding 2 polynomials
	def __add__(self, other):
		return self.monos + other.monos

	def __str__(self):
		s = ""
		for m in self.monos:
			s += str(m) + " + "
		return s[:-3]

class Mono_in_X:
	# Each monomial is attached with a coefficient
	# Format:  Mono_in_X( coefficient, ((Xₗₖ), exponent), ... )

	def __init__(self, c, *xs):
		self.coefficient = c
		self.xs = xs

	# **** Adding 2 monomials (may return polynomial)
	def __add__(self, other):
		# check if their exponents are equal
		if self.xs != other.xs:
			# return new polynomial
			return Poly_in_X(self, other)
		else:
			# return new monomial
			return Mono_in_X(self.coefficient + other.coefficient, \
				*self.xs)

	# **** Multiplying 2 monomials (result is always monomial)
	def __mul__(self, other):
		# collect same variables, assume vars are sorted in lexical order
		x3 = []
		L1 = len(self.xs)
		L2 = len(other.xs)
		i = j = 0
		while i < L1 or j < L2:
			x1 = self.xs[i][0] if i < L1 else (100,100)
			x2 = other.xs[j][0] if j < L2 else (100,100)
			if x1 == x2:
				x3.append((x1, self.xs[i][1] + other.xs[j][1]))
				i += 1
				j += 1
			elif x2 < x1:
				x3.append(other.xs[j])
				j += 1
			elif x1 < (100,100):
				x3.append(self.xs[i])
				i += 1
		return Mono_in_X(self.coefficient * other.coefficient, \
			*x3)

	def __str__(self):
		idx = ""
		for x in self.xs:
			idx += " X"
			idx += subscript(x[0][0])
			idx += subscript(x[0][1])
			idx += superscript(x[1])
		return str(self.coefficient) + idx

# Same shit, repeated for W:

class Poly_in_W:
	# A polynomial is just a sum of monomials
	def __init__(self, *monos):
		self.monos = monos

	# **** Adding 2 polynomials
	def __add__(self, other):
		return self.monos + other.monos

	def __str__(self):
		s = ""
		for m in self.monos:
			s += str(m) + " + "
		return "\u001b[36m{" + s[:-3] + "}\u001b[0m"

class Mono_in_W:
	# Each monomial is attached with a coefficient
	# Format:  Mono_in_W( coefficient, ((ₗₖWᵢⱼ), exponent), ... )
	def __init__(self, c, *ws):
		self.coefficient = c
		self.ws = ws

	# **** Adding 2 monomials (may return polynomial)
	def __add__(self, other):
		# check if their vars & exponents are equal
		if self.ws != other.ws:
			# return new polynomial
			return Poly_in_W(self, other)
		else:
			# return new monomial
			return Mono_in_W(self.coefficient + other.coefficient, \
				*self.ws)

	# **** Multiplying 2 monomials (result is always monomial)
	def __mul__(self, other):
		# collect same variables, assume vars are sorted in lexical order
		w3 = []
		L1 = len(self.ws)
		L2 = len(other.ws)
		i = j = 0
		while i < L1 or j < L2:
			w1 = self.ws[i][0] if i < L1 else None
			w2 = other.ws[j][0] if j < L2 else None
			if w1 == w2:
				w3.append((w1, self.ws[i][1] + other.ws[j][1]))
				i += 1
				j += 1
			elif w1 > w2:
				w3.append(other.ws[j])
				j += 1
			else:
				w3.append(self.ws[i])
				i += 1
		return Mono_in_W(self.coefficient * other.coefficient, \
			*w3)

	def __str__(self):
		idx = ""
		for w in self.ws:
			idx += ' ' + subscript(w[0][0])
			idx += subscript(w[0][1])
			idx += "W"
			idx += subscript(w[0][2])
			idx += subscript(w[0][3])
			idx += superscript(w[1])
		return str(self.coefficient) + idx

# **** Format:  Mono_in_X( coefficient, ((Xₗₖ), exponent), ... )
mono1 = Mono_in_X(3, ((1, 1), 2), ((2, 1), 2))
mono2 = Mono_in_X(2, ((1, 1), 1))
mono3 = Mono_in_X(7, ((1, 1), 1))
print(mono1)
print(mono1 + mono2)
print(mono2 + mono3)
print(mono1 * mono2)

# **** Format:  Mono_in_W( coefficient, (ₗₖWᵢⱼ, exponent), ... )
coeff1 = Mono_in_W(3, ((1, 1, 2, 1), 2), ((2, 1, 1, 1), 2))
coeff2 = Mono_in_W(4, ((1, 1, 2, 1), 3), ((2, 1, 1, 1), 1))
print(coeff1)
print(coeff2)
print(coeff1 * coeff2)
print(coeff1 + coeff2)

exit(0)

print("N = ?", end="")
N = int(input())

y = [[] for x in range(N)]

for k in range(0, N):
	# yₖ = Aₖ x x + Bₖ x + Cₖ
	#    = Σ (Aₖ x)ᵢ xᵢ + Σ Bₖᵢ xᵢ + Cₖ
	#    = Σⱼ (Σᵢ Aₖᵢⱼ xᵢ)ⱼ xⱼ + Σⱼ Bₖⱼ xⱼ + Cₖ
	for j in range(0, N):
		ΣBx += B[k, j] * x[j]
	y[k] = ΣBx + C[k]





# There are N x N x N = N^3 weights in the 3D matrix A
colors = [[i] for i in range(0, N **3)]

def find_index(z,y,x):
	return z * N * N + y * N + x

def find_zyx(index):
	z = index // (N * N)
	y = (index % (N * N)) // N
	x = index % N
	return (z,y,x)

# =================================
# find the left color in the list
# find the right color in the list
# join the 2 lists
def make_same_color(left, right):
	print(left, "=", right, end=":   ")
	global colors
	colors2 = []
	temp1 = temp2 = []
	for group in colors:
		if left in group:
			temp1 = group
		elif right in group:
			temp2 = group
		else:
			colors2.append(group)
	temp = temp1 + temp2
	print (temp)
	colors2.append(temp)
	colors = colors2

# 1st equation
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0, N):
				if i != h and i != k and j != h and j != k:
					left = find_index(h,i,j)
					right = find_index(k,i,j)
					make_same_color(left, right)

for h in range(0, N):
	for k in range(0, N):

		# diagonal equation #1
		left = find_index(h,h,h)
		right = find_index(k,k,k)
		make_same_color(left, right)

		# diagonal equation #2
		left = find_index(h,k,k)
		right = find_index(k,h,h)
		make_same_color(left, right)

# "missing" equations
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				# 1
				left = find_index(h,k,j)
				right = find_index(k,h,j)
				make_same_color(left, right)

				# 2
				left = find_index(h,h,j)
				right = find_index(k,k,j)
				make_same_color(left, right)

				# 3
				left = find_index(h,j,k)
				right = find_index(k,j,h)
				make_same_color(left, right)

				# 4
				left = find_index(h,j,h)
				right = find_index(k,j,k)
				make_same_color(left, right)

# ============ fill colors with values =============

A = np.zeros((N, N, N))

for group in colors:
	group.sort()					# sort the colors as well
	β = np.random.rand()
	for index in group:
		(z,y,x) = find_zyx(index)
		A[z][y][x] = β

print("\nColors = ", colors)

# ============ enforce additive constraints while respecting colors ===============

print("\nEnforcing 'additive' constraint while respecting colors:")

# Find representative in equivalence class (ie, smallest member)
def find_rep(z,y,x):
	idx = find_index(z,y,x)
	for group in colors:
		if idx in group:
			return group[0]			# assume colors are sorted
	return -1						# this indicates an error

print("Finding pairs....")
pairs = []
for h in range(0, N):
	for k in range(0, N):
		if h < k:					# also excluding h = k
			# a + b = c + d
			a = find_rep(k,k,h)
			b = find_rep(k,h,k)
			c = find_rep(h,k,h)
			d = find_rep(h,h,k)
			# sort order within each pair:
			left =  [a,b] if a < b else [b,a]
			right = [c,d] if c < d else [d,c]
			if pairs != [] and (not left in pairs) and (not right in pairs):
				print("ERROR:  additive constraints not a chain")
			if (not left in pairs):
				pairs.append(left)
			if (not right in pairs):
				pairs.append(right)

			print("{:d} {:d} {:d} ({:2d}) + {:d} {:d} {:d} ({:2d}) = ".format(k,k,h, find_rep(k,k,h), k,h,k, find_rep(k,h,k)),
				"{:d} {:d} {:d} ({:2d}) + {:d} {:d} {:d} ({:2d})".format(h,k,h, find_rep(h,k,h), h,h,k, find_rep(h,h,k)))

print("pairs = ", pairs)

print("Setting pairs....")
β = np.random.rand()
additive_colors = 0
for pair in pairs:
	additive_colors += 1
	α = np.random.rand()
	i = pair[0]
	# all entries of the same color as i = A[?,?,?] has to be changed as well
	for group in colors:
		if i in group:
			for j in group:
				(z,y,x) = find_zyx(j)
				A[z,y,x] = α

	i = pair[1]
	# all entries of the same color as i = A[?,?,?] has to be changed as well
	for group in colors:
		if i in group:
			for j in group:
				(z,y,x) = find_zyx(j)
				A[z,y,x] = 2 * β - α

print("\nResult: A =\n", A)

print("\n# colors = ", len(colors), " - additive constraint = ", additive_colors)

num_colors = len(colors) - additive_colors
print("\n# colors = ", num_colors, "of", N**3, "=", "{:.1f}".format(num_colors * 100.0 / N**3),\
	end="%\n")

# =========== verifications =============

print("\nNumerically counting # colors = ", end="")
numeric_colors = []
for k in range(0, N):
	for i in range(0, N):
		for j in range(0, N):
			a = A[k,i,j]
			matched = False
			for x in numeric_colors:
				if abs(a - x) < 1.0e-14:
					matched = True
			if not matched:
				numeric_colors.append(a)

print(len(numeric_colors))
print(numeric_colors)

num_Errors = 0

print("\nVerifying 'missing' equations....")
def error_missing(typ, a1,a2,a3, b1,b2,b3):
	num_Errors += 1
	print("type {:d}  A[{:d}][{:d}][{:d}] ≠ A[{:d}][{:d}][{:d}]".format(typ, a1,a2,a3,b1,b2,b3),\
		end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3], A[b1][b2][b3]))

for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				if A[h][k][j] != A[k][h][j]:
					error_missing(1, h,k,j,   k,h,j)
				if A[h][h][j] != A[k][k][j]:
					error_missing(2, h,h,j,   k,k,j)
				if A[h][j][k] != A[k][j][h]:
					error_missing(3, h,j,k,   k,j,h)
				if A[h][j][h] != A[k][j][k]:
					error_missing(4, h,j,h,   k,j,k)

print("\nVerifying 'additive' constraint....")

def error_additive(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3):
	global num_Errors
	num_Errors += 1
	print("{:d},{:d},{:d} + {:d},{:d},{:d} ≠ {:d},{:d},{:d} + {:d},{:d},{:d}".\
		format(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3), end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3] + A[b1][b2][b3], A[c1][c2][c3] + A[d1][d2][d3]))

for h in range(0, N):
	for k in range(0, N):
		if A[k][k][h] + A[k][h][k] != A[h][k][h] + A[h][h][k]:
			error_additive(k,k,h,  k,h,k,   h,k,h,   h,h,k)

print("\nVerifying 1st equation....")

def error_1st(a1,a2,a3, b1,b2,b3):
	num_Errors += 1
	print("{:d},{:d},{:d} ≠ {:d},{:d},{:d}".\
		format(a1,a2,a3, b1,b2,b3), end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3], A[b1][b2][b3]))

for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					if A[k][i][j] != A[h][i][j]:
						error_1st(k,i,j, h,i,j)

print("\nErrors detected = ", num_Errors)

print("\nTesting....")
debugFlag = False

for i in range(0, 10):				# repeat test 10 times

	x = np.random.rand(N)

	# permute x
	σ = np.random.permutation(N)
	σx = x[σ]

	Y = np.zeros(N)
	Y2 = np.zeros(N)

	for k in range(0, N):
		B_k = A[k].dot(x)
		# print("B_k = ", B_k)
		Y[k] = B_k.dot(x)

		C_k = A[k].dot(σx)
		Y2[k] = C_k.dot(σx)

	σY = Y[σ]					# real answer

	if debugFlag:
		print("\nx   =", x)
		print("σ·x =", σx)
		print("σ   =", σ)
		print("A x x   =", Y)
		print("A σx σx =", Y2)
		print("σ A x x =", σY)

	rms = 0.0					# root mean square error
	for j in range(0, N):
		rms += (Y2[j] - σY[j])**2
	rms = np.sqrt(rms / N)
	print("RMS error = ", rms)
