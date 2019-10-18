from .shape import ConstraintBoundaryShape

class ConstraintGlyph(ConstraintBoundaryShape):
	def __init__(self):
		super().__init__()

		componentPrefix = self.getComponentPrefix()

	def getComponentName(self):
		return "glyph"

	def resolve(self, uuid):
		for component in self.components:
			c = componenet.resolve(uuid)
			if c != None:
				return c
		return None

	def setComponents(self, components):
		self.components = components

	def getComponents(self):
		return self.components

	def getMargin(self):
		return self.getOccupationBoundary()

	def appendConstraints(self, problem):
		super().appendConstraints(problem)

		drawingGlyphPolicy = problem.getDrawingGlyphPolicy()
		size = drawingGlyphPolicy.getGlyphSize()
		marginHorizontal = drawingGlyphPolicy.getMarginHorizontal()
		marginVertical = drawingGlyphPolicy.getMarginVertical()

		problem.appendConstraint(self.getVarOccupationBoundaryLeft() - 0 == marginHorizontal)
		problem.appendConstraint(self.getVarOccupationBoundaryTop() - 0 == marginVertical)
		problem.appendConstraint(size[0] - self.getVarOccupationBoundaryRight() == marginHorizontal)
		problem.appendConstraint(size[1] - self.getVarOccupationBoundaryBottom() == marginVertical)

	def appendChildrenProblemTo(self, problem):
		super().appendChildrenProblemTo(problem)

		drawingGlyphPolicy = problem.getDrawingGlyphPolicy()

		for component in self.getComponents():
			subProblem = component.generateProblem(drawingGlyphPolicy)
			problem.appendProblem(subProblem)

