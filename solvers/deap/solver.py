from yong8.solver import AbsGlyphSolver

class DeapGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()

	def useCustomAlgebra(self):
	       return False

	def generateSolverVariable(self, totalName):
	       import sympy as sp
	       return sp.Symbol(totalName)

	def doSolve(self, problem):
		from deap_solver import deapSolve

		symbols = problem.getSymbols()
		variables = problem.getVariables()
		result =  deapSolve(variables, problem.getConstraints(), problem.getMaximizeObjective())

		solution = dict(zip(symbols, result))
		return solution

Solver = DeapGlyphSolver
