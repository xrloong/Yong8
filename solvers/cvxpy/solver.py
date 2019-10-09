from yong8.solver import AbsGlyphSolver
from yong8.solver import AbsVariableGenerator

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
			solutions[symbol] = value

		return solutions

Solver = lambda: CvxpyGlyphSolver.generateInstanceByECOS()
