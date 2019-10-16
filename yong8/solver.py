import abc

from .constants import Optimization
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
	def __init__(self, glyphSolver):
		self.glyphSolver = glyphSolver
		self.useCustomAlgebra = self.glyphSolver.useCustomAlgebra()
		self.solverVariableMap = {}

	def getSolverVariable(self, symbol):
		return self.solverVariableMap[symbol]

	def convert(self, problem):
		solverProblem = SolverProblem()

		symbols = []
		variables = []

		variableCounter = 0
		for variable in problem.getVariables():
			symbol = variable.getSymExpr()

			variableOutName = symbol.name
			variableInName = "x{0}".format(variableCounter)

			variableCounter += 1

			solverVariable = self.glyphSolver.generateSolverVariable(variableInName)
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

class AbsGlyphSolver(object, metaclass=abc.ABCMeta):
	def __init__(self):
		self.problem = Problem()

	def useCustomAlgebra(self):
		return True

	def generateSolverVariable(self, totalName):
		raise NotImplementedError('users must define generateSolverVariable() to use this base class')

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

	def solveProblem(self, problem: Problem):
		self.appendProblem(problem)
		self.solve()

	def solve(self):
		problemConverter = SolverProblemConverter(self)

		problem = self.problem
		solverProblem = problemConverter.convert(problem)

		solutions = self.doSolve(solverProblem)

		for variable in problem.getVariables():
			symbol = variable.getSymExpr()
			solverVariable = problemConverter.solverVariableMap[symbol]
			value = solutions[symbol]
			variable.setValue(value)

	def doSolve(self, problem):
		raise NotImplementedError('users must define solve() to use this base class')

