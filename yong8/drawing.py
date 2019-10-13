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

	def solveProblem(self, problem):
		self.glyphSolver.appendProblem(problem)
		self.glyphSolver.solve()

