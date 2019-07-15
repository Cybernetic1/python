# Polynomial algebra -- programmatically compute invariant weight colors
# ======================================================================

# TO-DO:
# * multiply monomials in X with monomials in W

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
		return str(self.coefficient) + idx

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

print("N = ? ", end="")
# N = int(input())
N = 3

y = [0] * N							# prepare vector y

x = [0] * N							# prepare vector x
for k in range(0, N):
	x[k] = Mono_in_X(1, ((1, k), 1))

B = [[0] * N for i in range(N)]		# prepare 2D array B
for k in range(0, N):
	for j in range(0, N):
		B[k][j] = Mono_in_W(1, ((1, k, j, 0), 1))

C = [0] * N							# prepare vector C
for k in range(0, N):
	C[k] = Mono_in_W(1, ((1, k, 0, 0), 1))

for k in range(0, N):
	# yₖ = Aₖ x x + Bₖ x + Cₖ
	#    = Σ (Aₖ x)ᵢ xᵢ + Σ Bₖᵢ xᵢ + Cₖ
	#    = Σⱼ (Σᵢ Aₖᵢⱼ xᵢ)ⱼ xⱼ + Σⱼ Bₖⱼ xⱼ + Cₖ
	ΣBX = Poly_in_X(Mono_in_X(0))
	for j in range(0, N):
		print(x[j])
		print(B[k][j])
		BX = B[k][j] * x[j]
		print(type(BX))
		print("BX.xs = ", BX.xs)
		print("BX.coefficient = ", BX.coefficient)
		print(BX)
		ΣBX_new = ΣBX + BX
		ΣBX = ΣBX_new
	y[k] = ΣBX + C[k]
	print(y[k])
