from yong8.solver import AbsGlyphSolver
from yong8.solver import AbsVariableGenerator

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
			solutions[symbol] = value

		return solutions

Solver = lambda: PuLPGlyphSolver.generateInstanceByGLPK()
