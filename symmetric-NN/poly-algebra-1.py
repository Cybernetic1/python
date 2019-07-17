# Polynomial algebra (1) -- programmatically compute invariant weight colors
# ==========================================================================
# This version succeeds in performing one LINEAR matrix multiplication

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

# About matrix indices:
# let x be x[0...n] where x[0] ≡ 1
# W[l,k,j,i] where  l = layer 0...L
#					k = for next layer's k-th component
#					if k = 0 means IGNORED
#					if i = 0 means LINEAR term
#					if j = i = 0 means CONSTANT term

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
		if type(other) == Mono_in_X:
			return self + Poly_in_X(other)
		else:
			# TO-DO: Collect like terms
			return Poly_in_X(*self.monos, *other.monos)

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
			if x[0] != (0,0):
				idx += " X"
				idx += subscript(x[0][0])
				idx += subscript(x[0][1])
				idx += superscript(x[1])
		c = str(self.coefficient) if self.coefficient != 0 else ''
		return c + idx

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
		return "{" + s[:-3] + "}"

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
	# We always use "left" multiplication of W with X, ie W∙X
	def __mul__(self, other):
		if type(other) == Mono_in_X:
			# Return Mono_in_X, with W appearing in the coefficient
			return Mono_in_X(Mono_in_W(other.coefficient * self.coefficient, \
					*self.ws), \
				*other.xs)
			return Mono_in_X(Mono_in_W(other.coefficient * self.coefficient, \
					self.ws), \
				*other.xs)
		else:
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
		c = str(self.coefficient) if self.coefficient != 1 else ''
		return "\u001b[36m" + c + idx + "\u001b[0m"

print("Testing...")

# **** Format:  Mono_in_X( coefficient, ((Xₗₖ), exponent), ... )
mono1 = Mono_in_X(3, ((1, 1), 2), ((2, 1), 2))
mono2 = Mono_in_X(2, ((1, 1), 1))
mono3 = Mono_in_X(7, ((1, 1), 1))
print("m₁ = ", mono1)
print("m₂ = ", mono2)
print("m₃ = ", mono3)
print("m₁ + m₂ = ", mono1 + mono2)
print("m₂ + m₃ = ", mono2 + mono3)
print("m₁ m₂ = ", mono1 * mono2)

# **** Format:  Mono_in_W( coefficient, (ₗₖWᵢⱼ, exponent), ... )
coeff1 = Mono_in_W(3, ((1, 1, 2, 1), 2), ((2, 1, 1, 1), 2))
coeff2 = Mono_in_W(4, ((1, 1, 2, 1), 3), ((2, 1, 1, 1), 1))
print("A₁ = ", coeff1)
print("A₂ = ", coeff2)
print("A₁ A₂ = ", coeff1 * coeff2)
print("A₁ + A₂ = ", coeff1 + coeff2)

print("\nN = ? ", end="")
# N = int(input())
N = 3
print(N)

y = [None] * (N + 1)							# prepare vector y

x = [None] * (N + 1)							# prepare vector x
for k in range(0, N + 1):
	x[k] = Mono_in_X(1, ((0, k), 1))

# prepare 3D array W (full layers would be 4D)
W = [[[None for i in range(N + 1)] for j in range(N + 1)] for k in range(N + 1)]
for k in range(0, N + 1):
	for j in range(0, N + 1):
		for i in range(0, N + 1):
			W[k][j][i] = Mono_in_W(1, ((0, k, j, i), 1))

# The 2D array B (which represents the LINEAR part) would have elements B[k][j] = W[k][j][0]
# 	where k,j ranges from 1...N

# The 1D vector C (which represents the CONSTANT term) would be the element C[k] = W[k][0][0]
#	where k ranges from 1...N

# **** Try calculating the LINEAR part ****
for k in range(1, N + 1):
	# yₖ = Aₖ x x + Bₖ x + Cₖ
	#    = Σ (Aₖ x)ᵢ xᵢ + Σ Bₖᵢ xᵢ + Cₖ
	#    = Σⱼ (Σᵢ Aₖᵢⱼ xᵢ)ⱼ xⱼ + Σⱼ Bₖⱼ xⱼ + Cₖ
	ΣBX = Poly_in_X()							# empty polynomial
	for j in range(0, N + 1):					# this includes the CONSTANT term
		# print(x[j])
		# print(W[k][j][0])
		# BX = W[k][j][0] * x[j]
		# print(type(BX))
		# print("BX.xs = ", BX.xs)
		# print("BX.coefficient = ", BX.coefficient)
		# print(BX)
		ΣBX += W[k][j][0] * x[j]
	y[k] = ΣBX
	print("y" + subscript(k) + " =", y[k])
