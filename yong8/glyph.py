from injector import inject

from .shape import ConstraintBoundaryShape

class ConstraintGlyph(ConstraintBoundaryShape):
	@inject
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
		glyphSolver = self.getVariableGenerator()
		return (glyphSolver.interpreteVariable(self.marginLeft),
			glyphSolver.interpreteVariable(self.marginTop),
			glyphSolver.interpreteVariable(self.marginRight),
			glyphSolver.interpreteVariable(self.marginBottom))

	def appendVariables(self, problem):
		super().appendVariables(problem)
		for component in self.getComponents():
			component.appendVariables(problem)

	def appendConstraints(self, problem):
		super().appendConstraints(problem)

		drawingGlyphPolicy = problem.getDrawingGlyphPolicy()
		size = drawingGlyphPolicy.getGlyphSize()
		marginHorizontal = drawingGlyphPolicy.getMarginHorizontal()
		marginVertical = drawingGlyphPolicy.getMarginVertical()

		problem.constraintsEq(self.getVarExtensionBoundaryLeft(), 0)
		problem.constraintsEq(self.getVarExtensionBoundaryTop(), 0)
		problem.constraintsEq(self.getVarExtensionBoundaryRight(), size[0])
		problem.constraintsEq(self.getVarExtensionBoundaryBottom(), size[1])
		problem.constraintsEq(self.getVarOccupationBoundaryLeft() - self.getVarExtensionBoundaryLeft(), marginHorizontal)
		problem.constraintsEq(self.getVarOccupationBoundaryTop() - self.getVarExtensionBoundaryTop(), marginVertical)
		problem.constraintsEq(self.getVarExtensionBoundaryRight() - self.getVarOccupationBoundaryRight(), marginHorizontal)
		problem.constraintsEq(self.getVarExtensionBoundaryBottom() - self.getVarOccupationBoundaryBottom(), marginVertical)
		for component in self.components:
			component.appendConstraints(problem)

	def appendObjective(self, problem):
		super().appendObjective(problem)

		for component in self.components:
			component.appendObjective(problem)

