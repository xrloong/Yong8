class Problem:
	def __init__(self):
		self.symbols = []
		self.variableMap = {}
		self.variableInNameMap = {}
		self.variableOutNameMap = {}

		self.symVariables = []
		self.symConstraints = []
		self.symObjectives = []

		self.variableCounter = 0

		self.constrains = 0
		self.objective = 0

	def generateVariable(self, prefix, name):
		variableOutName = prefix+"."+name
		variableInName = "x{0}".format(self.variableCounter)

		from .symbol import Symbol
		symbol = Symbol(variableInName)

		self.symbols.append(symbol)
		self.variableInNameMap[symbol] = variableInName
		self.variableOutNameMap[symbol] = variableOutName

		self.variableCounter += 1
		return symbol

	def setSolverVariable(self, symbol, solverVariable):
		self.variableMap[symbol]=solverVariable

	def getSolverVariable(self, symbol):
		return self.variableMap[symbol]

	def getVariableInName(self, symbol):
		return self.variableInNameMap[symbol]

	def setConstraints(self, constraints):
		self.constraints = constraints

	def setObjective(self, objective):
		self.objective = objective

	def getConstraints(self):
		return self.constraints

	def getObjective(self):
		return self.objective

	def addVariable(self, variable):
		self.symVariables.append(variable)

	def appendConstraint(self, constraint):
		self.symConstraints.append(constraint)

	def appendObjective(self, objective):
		self.symObjectives.append(objective)

	def getSymVariables(self):
		return self.symVariables

	def getSymConstraints(self):
		return self.symConstraints

	def getSymObjectives(self):
		return self.symObjectives

