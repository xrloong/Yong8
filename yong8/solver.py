import abc

class AbsVariableGenerator(object, metaclass=abc.ABCMeta):
	def useCustomAlgebra(self):
		return True

	def generateVariable(self, totalName):
		raise NotImplementedError('users must define generateVariable() to use this base class')

	def interpreteVariable(self, variable):
		raise NotImplementedError('users must define interpreteVariable() to use this base class')

class AbsGlyphSolver(object, metaclass=abc.ABCMeta):
	def __init__(self):
		self.variableGenerator = self.generateVariableGenerator();
		self.useCustomAlgebra = self.variableGenerator.useCustomAlgebra()

		self.variableMap = {}

		self.varibleInToOutMap = {}
		self.varibleOutToInMap = {}

		self.variableCounter = 0

	def getVariableGenerator(self):
		return self.variableGenerator

	def generateVariable(self, prefix, name):
		variableOutName = prefix+"."+name
		variableInName = "x{0}".format(self.variableCounter)
		self.variableCounter += 1

		from .symbol import Symbol
		symbol = Symbol(variableInName)

		solverVariable = self.variableGenerator.generateVariable(variableInName)

		self.variableMap[variableInName] = solverVariable
		self.varibleInToOutMap[variableInName] = variableOutName
		self.varibleOutToInMap[variableOutName] = variableInName

		return symbol

	def getVariableByInName(self, variableInName):
		return self.variableMap[variableInName]

	def interpreteVariable(self, variable):
		return self.variableGenerator.interpreteVariable(self.getSolverVariable(variable))

	def getSolverVariable(self, variable):
		return self.variableMap[variable.name]

	def convertSymExpr(self, symExpr):
		if symExpr.is_Number:
			return float(symExpr)
		elif symExpr.is_Relational:
			from .symbol import Le, Lt, Ge, Gt, Eq
			lhsConverted = self.convertSymExpr(symExpr.lhs)
			rhsConverted = self.convertSymExpr(symExpr.rhs)

			if isinstance(symExpr, Eq):
				if self.useCustomAlgebra:
					return lhsConverted == rhsConverted
				else:
					return Eq(lhsConverted, rhsConverted, evaluate=False)
			elif isinstance(symExpr, Lt):
				return lhsConverted < rhsConverted
			elif isinstance(symExpr, Le):
				return lhsConverted <= rhsConverted
			elif isinstance(symExpr, Gt):
				return lhsConverted > rhsConverted
			elif isinstance(symExpr, Ge):
				return lhsConverted >= rhsConverted

		elif symExpr.is_Symbol:
			variableName=symExpr.name
			return self.getVariableByInName(variableName)

		elif symExpr.is_Add:
			r = 0
			(c, exprs) = symExpr.as_coeff_add()
			r=self.convertSymExpr(c)
			for e in exprs:
				r = r+self.convertSymExpr(e)
			return r
		elif symExpr.is_Mul:
			r = 0
			(c, exprs) = symExpr.as_coeff_mul()
			r=self.convertSymExpr(c)
			for e in exprs:
				r = r*self.convertSymExpr(e)
			return r
		elif symExpr.is_Pow:
			(base, exp)=symExpr.as_base_exp()
			baseVariable = self.convertSymExpr(base)
			expValue = self.convertSymExpr(exp)
			return pow(baseVariable, expValue)
		else:
			return None

	def generateVariableGenerator(self):
		raise NotImplementedError('users must define generateVariableGenerator() to use this base class')
	def addVariable(self, variable):
		raise NotImplementedError('users must define addVariable() to use this base class')

	def appendConstraint(self, constraint):
		raise NotImplementedError('users must define appendConstraint() to use this base class')

	def appendObjective(self, objective):
		raise NotImplementedError('users must define appendObjective() to use this base class')

	def solve(self):
		raise NotImplementedError('users must define solve() to use this base class')

class CassowaryVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, totalName):
		from cassowary import Variable
		return Variable(totalName)

	def interpreteVariable(self, variable):
		return variable.value

class CassowaryGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()

		from cassowary import SimplexSolver
		self.solver = SimplexSolver()

	def generateVariableGenerator(self):
		return CassowaryVariableGenerator()

	def addVariable(self, variable):
		self.solver.add_var(self.getSolverVariable(variable))

	def appendConstraint(self, constraint):
		self.solver.add_constraint(self.convertSymExpr(constraint))

	def appendObjective(self, objective):
		from cassowary import STRONG
		self.solver.add_constraint(self.convertSymExpr(objective) >= 2**32, STRONG)

	def solve(self):
		# Cassowary use incremental solving.
		# It solves the problem during changing constraints.
		pass

class PuLPVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, totalName):
		from pulp import LpVariable
		return LpVariable(totalName)

	def interpreteVariable(self, variable):
		return variable.value()

class PuLPGlyphSolver(AbsGlyphSolver):
	def __init__(self, solver):
		super().__init__()

		from pulp import LpProblem
		from pulp import LpMaximize, LpMinimize

		self.prob = LpProblem("myProb", LpMaximize)
		self.solver =solver(msg=False)

	@classmethod
	def generateInstanceByGLPK(cls):
		from pulp import GLPK
		return PuLPGlyphSolver(GLPK)

	def generateVariableGenerator(self):
		return PuLPVariableGenerator()

	def addVariable(self, variable):
		self.prob.addVariable(self.getSolverVariable(variable))

	def appendConstraint(self, constraint):
		self.prob += self.convertSymExpr(constraint)

	def appendObjective(self, objective):
		convertedObjective = self.convertSymExpr(objective)
		if self.prob.objective != None:
			self.prob.objective = self.prob.objective + convertedObjective
		else:
			self.prob.objective = convertedObjective

	def solve(self):
		status = self.prob.solve(self.solver)

class CvxpyVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, totalName):
		from cvxpy import Variable
		return Variable()

	def interpreteVariable(self, variable):
		return variable.value.item()

class CvxpyGlyphSolver(AbsGlyphSolver):
	def __init__(self, solver):
		super().__init__()

		self.objective = 0
		self.constraints = []
		self.solver = solver

	@classmethod
	def generateInstanceByECOS(cls):
		from cvxpy import ECOS
		return CvxpyGlyphSolver(ECOS)

	def generateVariableGenerator(self):
		return CvxpyVariableGenerator()

	def addVariable(self, variable):
		pass

	def appendConstraint(self, constraint):
		self.constraints.append(self.convertSymExpr(constraint))

	def appendObjective(self, objective):
		self.objective += self.convertSymExpr(objective)

	def solve(self):
		from cvxpy import Problem
		from cvxpy import Maximize, Minimize
		prob = Problem(Maximize(self.objective), self.constraints)
		prob.solve(self.solver)

class DRealVariableGenerator(AbsVariableGenerator):
	def __init__(self):
		self.solution = {}

	def generateVariable(self, totalName):
		from dreal import Variable
		return Variable(totalName)

	def interpreteVariable(self, variable):
		return self.solution[variable]

	def setSolution(self, solution):
		self.solution = solution

class DRealGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()

		self.variables = []
		self.constraints = []
		self.objective = 0

	def generateVariableGenerator(self):
		return DRealVariableGenerator()

	def addVariable(self, variable):
		self.variables.append(variable)

	def appendConstraint(self, constraint):
		self.constraints.append(self.convertSymExpr(constraint))

	def appendObjective(self, objective):
		self.objective += self.convertSymExpr(objective)

	def solve(self):
		from dreal import Minimize
		from dreal import And

		result = Minimize(-self.objective, And(*self.constraints), 0)

		solution = {}
		for var, interval in result.items():
			solution[var] = interval.mid()

		self.variableGenerator.setSolution(solution)

class SciPyVariableGenerator(AbsVariableGenerator):
	def useCustomAlgebra(self):
		return False

	def generateVariable(self, totalName):
		import sympy as sp
		return sp.Symbol(totalName)

	def interpreteVariable(self, variable):
		return self.solution[variable]

	def setSolution(self, solution):
		self.solution = solution

class SciPyGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()

		self.variables = []
		self.constraints = []
		self.objective = 0

	def generateVariableGenerator(self):
		return SciPyVariableGenerator()

	def addVariable(self, variable):
		self.variables.append(variable)

	def appendConstraint(self, constraint):
		self.constraints.append(self.convertSymExpr(constraint))

	def appendObjective(self, objective):
		self.objective += self.convertSymExpr(objective)

	def solve(self):
		import sympy as sp
		import numpy as np
		import scipy.optimize as opt

		symVariables = self.variables
		symConstraints = self.constraints
		symObjective = self.objective

		lambdifiedObjective = sp.lambdify(symVariables, symObjective)
		objective = lambda params: lambdifiedObjective(*params)

		constraints = [
		]
		t = None
		f = None
		for c in symConstraints:
			if c.rel_op == '==':
				t="eq"
				f=c.lhs-c.rhs
			elif c.rel_op in ['<=', '<']:
				t="ineq"
				f=c.rhs-c.lhs
			elif c.rel_op in ['>=', '>']:
				t="ineq"
				f=c.lhs-c.rhs
			func = sp.lambdify(symVariables, f)
			constraint = {"type": t, "fun": lambda x: func(*x)}
			constraints.append(constraint)

#		jacF = [sp.lambdify(symVariables, symObjective.diff(x)) for x in symVariables]
#		jac = lambda x: np.asarray([l(*x) for l in jacF])

		x = [0 for i in range(len(symVariables))]
		# slsqp, trust-constr, trust-exact, trust-krylov
		results = opt.minimize(objective, x, method='slsqp', constraints=constraints, tol=1e-8)

		solution = dict(zip(symVariables, results.x))
		self.variableGenerator.setSolution(solution)

