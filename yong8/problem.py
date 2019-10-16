from .constants import Optimization
from .drawing import DrawingGlyphPolicy

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

	def appendObjective(self, objective, optimization: Optimization = Optimization.Maximize):
		self.objectives.append((optimization, objective))
		self.symObjectives.append((optimization, objective.getSymExpr()))

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

