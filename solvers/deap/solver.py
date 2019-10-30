from yong8.solver import AbsGlyphSolver

class DeapGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()
		self.boundContraints = []

	def generateSolverVariable(self, variableName, lowerBound=None, upperBound=None):
		import sympy as sp
		symbol = sp.Symbol(variableName)
		if lowerBound is not None:
			self.boundContraints.append(lowerBound <= symbol)
		if upperBound is not None:
			self.boundContraints.append(upperBound <= symbol)
		return symbol

	def constraintEq(self, lhs, rhs):
		import sympy as sp
		return sp.Eq(lhs, rhs, evaluate=False)

	def doSolve(self, problem):
		from deap_solver import deapSolve

		symbols = problem.getSymbols()
		variables = problem.getVariables()
		constraints = tuple(self.boundContraints) + tuple(problem.getConstraints())
		result =  deapSolve(variables, problem.getConstraints(), problem.getMaximizeObjective())

		solution = dict(zip(symbols, result))
		return solution

Solver = DeapGlyphSolver
