import abc

class Problem:
	def __init__(self):
		self.constrains = 0
		self.objective = 0

	def setConstraints(self, constraints):
		self.constraints = constraints

	def setObjective(self, objective):
		self.objective = objective

	def getConstraints(self):
		return self.constraints

	def getObjective(self):
		return self.objective

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

		self.symbols = []
		self.variableMap = {}
		self.variableInNameMap = {}
		self.variableOutNameMap = {}

		self.variables = []
		self.constraints = []
		self.objectives = []

		self.variableCounter = 0

	def getVariableGenerator(self):
		return self.variableGenerator

	def generateVariable(self, prefix, name):
		variableOutName = prefix+"."+name
		variableInName = "x{0}".format(self.variableCounter)

		from .symbol import Symbol
		symbol = Symbol(variableInName)

		self.symbols.append(symbol)
		self.variableInNameMap[symbol] = variableInName
		self.variableOutNameMap[symbol] = variableOutName

		self.variableCounter += 1
		return symbol

	def interpreteVariable(self, variable):
		return self.variableGenerator.interpreteVariable(self.getSolverVariable(variable))

	def getSolverVariable(self, variable):
		return self.variableMap[variable]

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
			return self.getSolverVariable(symExpr)

		elif symExpr.is_Add:
			(c, exprs) = symExpr.as_coeff_add()
			r=self.convertSymExpr(c)
			for e in exprs:
				r = r+self.convertSymExpr(e)
			return r
		elif symExpr.is_Mul:
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
		self.variables.append(variable)

	def appendConstraint(self, constraint):
		self.constraints.append(constraint)

	def appendObjective(self, objective):
		self.objectives.append(objective)

	def solve(self):
		for symbol in self.variables:
			variableInName = self.variableInNameMap[symbol]
			solverVariable = self.variableGenerator.generateVariable(variableInName)

			self.variableMap[symbol] = solverVariable

		constraints = [self.convertSymExpr(constraint) for constraint in self.constraints]
		objective = self.convertSymExpr(sum(self.objectives))

		problem = Problem()
		problem.setConstraints(constraints)
		problem.setObjective(objective)
		self.doSolve(problem)

	def doSolve(self, problem):
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

	def doSolve(self, problem):
		from cassowary import STRONG

		for constraint in problem.getConstraints():
			self.solver.add_constraint(constraint)

		self.solver.add_constraint(problem.getObjective() >= 2**32, STRONG)

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
		self.solver = solver(msg=False)

	@classmethod
	def generateInstanceByGLPK(cls):
		from pulp import GLPK
		return PuLPGlyphSolver(GLPK)

	def generateVariableGenerator(self):
		return PuLPVariableGenerator()

	def doSolve(self, problem):
		from pulp import LpProblem
		from pulp import LpMaximize, LpMinimize

		prob = LpProblem("myProb", LpMaximize)

		for constraint in problem.getConstraints():
			prob += constraint

		prob.objective = problem.getObjective()

		status = prob.solve(self.solver)

class CvxpyVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, totalName):
		from cvxpy import Variable
		return Variable()

	def interpreteVariable(self, variable):
		return variable.value.item()

class CvxpyGlyphSolver(AbsGlyphSolver):
	def __init__(self, solver):
		super().__init__()
		self.solver = solver

	@classmethod
	def generateInstanceByECOS(cls):
		from cvxpy import ECOS
		return CvxpyGlyphSolver(ECOS)

	def generateVariableGenerator(self):
		return CvxpyVariableGenerator()

	def doSolve(self, problem):
		from cvxpy import Problem
		from cvxpy import Maximize, Minimize
		prob = Problem(Maximize(problem.getObjective()), problem.getConstraints())
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

	def generateVariableGenerator(self):
		return DRealVariableGenerator()

	def doSolve(self, problem):
		from dreal import Minimize
		from dreal import And

		constraints = problem.getConstraints()
		objective = problem.getObjective()

		result = Minimize(-objective, And(*constraints), 0)

		solution = {}
		for var, interval in result.items():
			solution[var] = interval.mid()

		self.variableGenerator.setSolution(solution)

