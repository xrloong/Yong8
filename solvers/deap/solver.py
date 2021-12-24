from yong8.solver import AbsSolver

class DeapSolver(AbsSolver):
	def __init__(self):
		super().__init__()
		self.boundConstraints = []

	def generateSolverVariable(self, variableName, lowerBound=None, upperBound=None):
		import sympy as sp
		symbol = sp.Symbol(variableName)
		if lowerBound is not None:
			self.boundConstraints.append(lowerBound <= symbol)
		if upperBound is not None:
			self.boundConstraints.append(symbol <= upperBound)
		return symbol

	def constraintEq(self, lhs, rhs):
		import sympy as sp
		return sp.Eq(lhs, rhs, evaluate=False)

	def doSolve(self, problem):
		from deap_solver import deapSolve

		symbols = problem.getSymbols()
		variables = problem.getVariables()
		constraints = tuple(self.boundConstraints) + tuple(problem.getConstraints())
		result =  deapSolve(variables, constraints, problem.getMaximizeObjective())

		solution = dict(zip(symbols, result))
		return solution

Solver = DeapSolver
