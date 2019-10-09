from yong8.solver import AbsGlyphSolver
from yong8.solver import AbsVariableGenerator

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
			solutions[symbol] = value

		return solutions

Solver = Z3GlyphSolver
