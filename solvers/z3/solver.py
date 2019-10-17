from yong8.solver import AbsGlyphSolver

class Z3GlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()

	def generateSolverVariable(self, totalName):
		from z3 import Real
		return Real(totalName)

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
			solutions[symbol] = float(value.as_decimal(7)) if hasattr(value, 'as_decimal') else 0

		return solutions

Solver = Z3GlyphSolver
