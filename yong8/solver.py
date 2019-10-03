import abc

from .problem import Optimization
from .problem import Problem

class SolverProblem:
	def __init__(self):
		self.symbols = []
		self.variables = []
		self.constraints = []
		self.objectives = []
		self.solutions = {}

	def getSymbols(self):
		return self.symbols

	def getVariables(self):
		return self.variables

	def getConstraints(self):
		return self.constraints

	def getMaximizeObjective(self):
		objective = sum(objective[1] if objective[0]==Optimization.Maximize else -1 * objective[1] for objective in self.objectives)
		return objective

	def getMinimizeObjective(self):
		objective = sum(objective[1] if objective[0]==Optimization.Minimize else -1 * objective[1] for objective in self.objectives)
		return objective

	def queryVariableBySym(self, sym):
		return self.variableMap[sym]

	def setSymbolsAndVariables(self, symbols, variables):
		self.symbols = symbols
		self.variables = variables
		self.variableMap = dict(zip(symbols, variables))

	def setConstraints(self, constraints):
		self.constraints = constraints

	def setObjectives(self, objectives):
		self.objectives = objectives

class SolverProblemConverter:
	def __init__(self, variableGenerator):
		self.variableGenerator = variableGenerator
		self.useCustomAlgebra = self.variableGenerator.useCustomAlgebra()
		self.solverVariableMap = {}

	def getSolverVariable(self, symbol):
		return self.solverVariableMap[symbol]

	def convert(self, problem):
		solverProblem = SolverProblem()

		symbols = []
		variables = []
		for variable in problem.getVariables():
			symbol = variable.getSymExpr()
			variableInName = problem.getVariableInName(symbol)
			solverVariable = self.variableGenerator.generateVariable(variableInName)
			self.solverVariableMap[symbol] = solverVariable
			symbols.append(symbol)
			variables.append(solverVariable)

		constraints = [self.convertSymExpr(constraint) for constraint in problem.getSymConstraints()]
		objectives = [(objective[0], self.convertSymExpr(objective[1])) for objective in problem.getSymObjectives()]

		solverProblem.setSymbolsAndVariables(symbols, variables)
		solverProblem.setConstraints(constraints)
		solverProblem.setObjectives(objectives)
		return solverProblem

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

class AbsVariableGenerator(object, metaclass=abc.ABCMeta):
	def useCustomAlgebra(self):
		return True

	def generateVariable(self, totalName):
		raise NotImplementedError('users must define generateVariable() to use this base class')

class AbsGlyphSolver(object, metaclass=abc.ABCMeta):
	def __init__(self):
		self.problem = Problem()

	def generateVariable(self, prefix, name):
		return self.problem.generateVariable(prefix, name)

	def generateVariableGenerator(self):
		raise NotImplementedError('users must define generateVariableGenerator() to use this base class')

	def addVariable(self, variable):
		self.problem.addVariable(variable)

	def appendConstraint(self, constraint):
		self.problem.appendConstraint(constraint)

	def appendObjective(self, objective):
		self.problem.appendObjective(objective[1], objective[0])

	def appendProblem(self, problem):
		for variable in problem.getVariables():
			self.addVariable(variable)

		for constraint in problem.getConstraints():
			self.appendConstraint(constraint)

		for objective in problem.getObjectives():
			self.appendObjective(objective)

	def solve(self):
		variableGenerator = self.generateVariableGenerator();
		problemConverter = SolverProblemConverter(variableGenerator)

		problem = self.problem
		solverProblem = problemConverter.convert(problem)

		solutions = self.doSolve(solverProblem)

		for variable in problem.getVariables():
			symbol = variable.getSymExpr()
			solverVariable = problemConverter.solverVariableMap[symbol]
			value = solutions[solverVariable]
			variable.setValue(value)

	def doSolve(self, problem):
		raise NotImplementedError('users must define solve() to use this base class')

class CassowaryGlyphSolver(AbsGlyphSolver):
	class VariableGenerator(AbsVariableGenerator):
		def generateVariable(self, totalName):
			from cassowary import Variable
			return Variable(totalName)

	def __init__(self):
		super().__init__()

		from cassowary import SimplexSolver
		self.solver = SimplexSolver()

	def generateVariableGenerator(self):
		return CassowaryGlyphSolver.VariableGenerator()

	def doSolve(self, problem):
		from cassowary import STRONG

		for constraint in problem.getConstraints():
			self.solver.add_constraint(constraint)

		self.solver.add_constraint(problem.getMaximizeObjective() >= 2**32, STRONG)

		# Cassowary use incremental solving.
		# It solves the problem during changing constraints.

		solutions = {}
		for symbol in problem.getSymbols():
			variable = problem.queryVariableBySym(symbol)
			value = variable.value
			solutions[variable] = value

		return solutions

class PuLPGlyphSolver(AbsGlyphSolver):
	class VariableGenerator(AbsVariableGenerator):
		def generateVariable(self, totalName):
			from pulp import LpVariable
			return LpVariable(totalName)

	def __init__(self, solver):
		super().__init__()
		self.solver = solver(msg=False)

	@classmethod
	def generateInstanceByGLPK(cls):
		from pulp import GLPK
		return PuLPGlyphSolver(GLPK)

	def generateVariableGenerator(self):
		return PuLPGlyphSolver.VariableGenerator()

	def doSolve(self, problem):
		from pulp import LpProblem
		from pulp import LpMaximize, LpMinimize

		prob = LpProblem("myProb", LpMaximize)

		for constraint in problem.getConstraints():
			prob += constraint

		prob.objective = problem.getMaximizeObjective()

		status = prob.solve(self.solver)

		solutions = {}
		for symbol in problem.getSymbols():
			variable = problem.queryVariableBySym(symbol)
			value = variable.value()
			solutions[variable] = value

		return solutions

class CvxpyGlyphSolver(AbsGlyphSolver):
	class VariableGenerator(AbsVariableGenerator):
		def generateVariable(self, totalName):
			from cvxpy import Variable
			return Variable()

	def __init__(self, solver):
		super().__init__()
		self.solver = solver

	@classmethod
	def generateInstanceByECOS(cls):
		from cvxpy import ECOS
		return CvxpyGlyphSolver(ECOS)

	def generateVariableGenerator(self):
		return CvxpyGlyphSolver.VariableGenerator()

	def doSolve(self, problem):
		from cvxpy import Problem
		from cvxpy import Maximize, Minimize
		prob = Problem(Maximize(problem.getMaximizeObjective()), problem.getConstraints())
		prob.solve(self.solver)

		solutions = {}
		for symbol in problem.getSymbols():
			variable = problem.queryVariableBySym(symbol)
			value = variable.value.item()
			solutions[variable] = value

		return solutions

class DRealGlyphSolver(AbsGlyphSolver):
	class VariableGenerator(AbsVariableGenerator):
		def generateVariable(self, totalName):
			from dreal import Variable
			return Variable(totalName)

	def __init__(self):
		super().__init__()

	def generateVariableGenerator(self):
		return DRealGlyphSolver.VariableGenerator()

	def doSolve(self, problem):
		from dreal import Minimize
		from dreal import And

		constraints = problem.getConstraints()
		objective = problem.getMinimizeObjective()

		result = Minimize(objective, And(*constraints), 0)

		solutions = {}
		for var, interval in result.items():
			solutions[var] = interval.mid()

		return solutions

class Z3GlyphSolver(AbsGlyphSolver):
	class VariableGenerator(AbsVariableGenerator):
		def generateVariable(self, totalName):
			from z3 import Real
			return Real(totalName)

	def __init__(self):
		super().__init__()

	def generateVariableGenerator(self):
		return Z3GlyphSolver.VariableGenerator()

	def doSolve(self, problem):
		from z3 import Optimize

		variables = problem.getVariables()
		constraints = problem.getConstraints()
		objective = problem.getMaximizeObjective()

		opt = Optimize()
		for c in constraints:
			opt.add(c)

		opt.maximize(objective)
		opt.check()

		model = opt.model()

		solutions = {}
		for symbol in problem.getSymbols():
			variable = problem.queryVariableBySym(symbol)
			value = model[variable]
			solutions[variable] = value

		return solutions

