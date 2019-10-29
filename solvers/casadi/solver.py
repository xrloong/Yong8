from yong8.solver import AbsGlyphSolver

class CasADiGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()

		import casadi
		self.model = casadi.Opti()

	def generateSolverVariable(self, totalName):
		import casadi
		return self.model.variable()

	def constraintEq(self, lhs, rhs):
		return lhs+1 == rhs+1

	def doSolve(self, problem):
		import casadi

		variables = problem.getVariables()
		constraints = problem.getConstraints()
		objective = problem.getMinimizeObjective()

		extraV = []
		model = self.model
		extraVariableCount = max(len(variables), len(constraints)) - len(variables)
		for i in range(extraVariableCount):
			v=model.variable()
			extraV.append(v)
			model.subject_to(v <= v+1)

		model.minimize(objective)
		for c in constraints:
			model.subject_to(c)

		model.solver('ipopt')
		sol = model.solve()

		xopt = sol.value_variables()
		solutions = {}
		for symbol in problem.getSymbols():
			variable = problem.queryVariableBySym(symbol)
			value = sol.value(variable)
			solutions[symbol] = value

		return solutions

Solver = CasADiGlyphSolver

