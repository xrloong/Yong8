from yong8.solver import AbsGlyphSolver
from yong8.solver import AbsVariableGenerator

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

		variableToSymbolMap = {}
		for symbol in problem.getSymbols():
			variable = problem.queryVariableBySym(symbol)
			variableToSymbolMap[variable] = symbol

		solutions = {}
		for var, interval in result.items():
			symbol = variableToSymbolMap[var]
			solutions[symbol] = interval.mid()

		return solutions

Solver = DRealGlyphSolver
