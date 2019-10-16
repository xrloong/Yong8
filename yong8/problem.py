from .constants import Optimization
from .drawing import DrawingGlyphPolicy

class Objective:
	def __init__(self, function, optimization: Optimization = Optimization.Maximize):
		self.optimization = optimization
		self.function = function

	def getOptimization(self):
		return self.optimization

	def getFunction(self):
		return self.function

class Problem:
	def __init__(self, drawingGlyphPolicy: DrawingGlyphPolicy):
		self.symbols = []

		self.variables = []
		self.constraints = []
		self.objectives = []

		self.symVariables = []
		self.symConstraints = []
		self.symObjectives = []

		self.drawingGlyphPolicy = drawingGlyphPolicy

	def addVariable(self, variable):
		self.variables.append(variable)
		self.symVariables.append(variable.getSymExpr())

	def appendConstraint(self, constraint):
		self.constraints.append(constraint)
		self.symConstraints.append(constraint.getSymExpr())

	def appendObjective(self, objective: Objective):
		optimization = objective.getOptimization()
		function = objective.getFunction()
		self.objectives.append(objective)
		self.symObjectives.append((optimization, function.getSymExpr()))

	def _addAllVariables(self, variables):
		for variable in variables:
			self.addVariable(variable)

	def _appendAllConstraints(self, constraints):
		for constraint in constraints:
			self.appendConstraint(constraint)

	def _appendAllObjectives(self, objectives):
		for objective in objectives:
			self.appendObjective(objective)

	def appendProblem(self, problem):
		self._addAllVariables(problem.getVariables())
		self._appendAllConstraints(problem.getConstraints())
		self._appendAllObjectives(problem.getObjectives())

	def getVariables(self):
		return self.variables

	def getConstraints(self):
		return self.constraints

	def getObjectives(self):
		return self.objectives

	def getSymVariables(self):
		return self.symVariables

	def getSymConstraints(self):
		return self.symConstraints

	def getSymObjectives(self):
		return self.symObjectives

	def getDrawingGlyphPolicy(self):
		return self.drawingGlyphPolicy

