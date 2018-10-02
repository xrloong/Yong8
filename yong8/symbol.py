import abc

from sympy import Eq, Le, Lt, Ge, Gt

class A:
	def __init__(self, symexpr = 0):
		self.symexpr = symexpr

	def __str__(self):
		return str(self.symexpr)

	def setSymExpr(self, symexpr):
		self.symexpr = symexpr

	def getSymExpr(self):
		return self.symexpr

	def __neg__(self):
		symexpr = -self.getSymExpr()
		return E(symexpr)

	def __radd__(self, other):
		return self.__add__(other)

	def __add__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = self.getSymExpr() + other
		else:
			symexpr = self.getSymExpr() + other.getSymExpr()
		return E(symexpr)

	def __rsub__(self, other):
		return -self+other

	def __sub__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = self.getSymExpr() - other
		else:
			symexpr = self.getSymExpr() - other.getSymExpr()
		return E(symexpr)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __mul__(self, mul):
		if isinstance(mul, int) or isinstance(mul, float):
			symexpr = self.getSymExpr() * mul
		else:
			symexpr = self.getSymExpr() * mul.getSymExpr()
		return E(symexpr)

	def __rtruediv__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = other / self.getSymExpr()
		else:
			symexpr = other.getSymExpr() / self.getSymExpr()
		return E(symexpr)

	def __truediv__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = self.getSymExpr() / other
		else:
			symexpr = self.getSymExpr() / other.getSymExpr()
		return E(symexpr)

	def __eq__(self, other):
		from sympy import Eq
		if isinstance(other, int) or isinstance(other, float):
			symexpr = Eq(self.getSymExpr(), other, evaluate=False)
		else:
			symexpr = Eq(self.getSymExpr(), other.getSymExpr(), evaluate=False)
		return C(symexpr)

	def __ne__(self, other):
		from sympy import Ne
		if isinstance(other, int) or isinstance(other, float):
			symexpr = Ne(self.getSymExpr(), other)
		else:
			symexpr = Ne(self.getSymExpr(), other.getSymExpr())
		return C(symexpr)

	def __ge__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = self.getSymExpr() >= other
		else:
			symexpr = self.getSymExpr() >= other.getSymExpr()
		return C(symexpr)

	def __gt__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = self.getSymExpr() > other
		else:
			symexpr = self.getSymExpr() > other.getSymExpr()
		return C(symexpr)

	def __le__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = self.getSymExpr() <= other
		else:
			symexpr = self.getSymExpr() <= other.getSymExpr()
		return C(symexpr)

	def __lt__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			symexpr = self.getSymExpr() < other
		else:
			symexpr = self.getSymExpr() < other.getSymExpr()
		return C(symexpr)

class V(A):
	def __init__(self, name):
		from sympy import Symbol

		self.name = name
		super().__init__(Symbol(name))

class E(A):
	def __init__(self, symexpr):
		super().__init__(symexpr)

class C(A):
	def __init__(self, symexpr):
		super().__init__(symexpr)
