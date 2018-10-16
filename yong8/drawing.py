from injector import inject

from .constants import GlyphSolver

class DrawingGlyphPolicy:
	def __init__(self):
		pass

	def getGlyphSize(self):
		return (255, 255)

	def getMarginHorizontal(self):
		return 40

	def getMarginVertical(self):
		return 20

class DrawingPolicy:
	def __init__(self):
		self.drawingGlyphPolicy = DrawingGlyphPolicy()

	def getDrawingGlyphPolicy(self):
		return self.drawingGlyphPolicy

class ConstraintDrawingSystem:
	@inject
	def __init__(self, glyphSolver: GlyphSolver):
		self.glyphSolver = glyphSolver

		self.drawingPolicy = DrawingPolicy()

	def getDrawingPolicy(self):
		return self.drawingPolicy

	def getDrawingGlyphPolicy(self):
		return self.drawingPolicy.getDrawingGlyphPolicy()

	def getGlyphSolver(self):
		return self.glyphSolver

	def getVariableGenerator(self):
		return self.glyphSolver.getVariableGenerator()

	def addVariable(self, variable):
		self.glyphSolver.addVariable(variable)

	def appendConstraint(self, constraint):
		self.glyphSolver.appendConstraint(constraint)

	def appendObjective(self, objective):
		self.glyphSolver.appendObjective(objective)

	def appendProblem(self, problem):
		for variable in problem.getVariables():
			self.addVariable(variable)

		for constraint in problem.getConstraints():
			self.appendConstraint(constraint)

		for objective in problem.getObjectives():
			self.appendObjective(objective)

	def solve(self):
		self.glyphSolver.solve()

