from injector import inject

from .shape import ConstraintBoundaryShape

class ConstraintGlyph(ConstraintBoundaryShape):
	@inject
	def __init__(self):
		super().__init__()

		componentPrefix = self.getComponentPrefix()

	def getComponentName(self):
		return "glyph"

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

	def appendVariables(self, drawingSystem):
		super().appendVariables(drawingSystem)
		for component in self.getComponents():
			component.appendVariables(drawingSystem)

	def appendConstraints(self, drawingSystem):
		super().appendConstraints(drawingSystem)

		drawingGlyphPolicy = drawingSystem.getDrawingGlyphPolicy()
		size = drawingGlyphPolicy.getGlyphSize()
		marginHorizontal = drawingGlyphPolicy.getMarginHorizontal()
		marginVertical = drawingGlyphPolicy.getMarginVertical()

		drawingSystem.appendConstraint(self.getVarExtensionBoundaryLeft() == 0)
		drawingSystem.appendConstraint(self.getVarExtensionBoundaryTop() == 0)
		drawingSystem.appendConstraint(self.getVarExtensionBoundaryRight() == size[0])
		drawingSystem.appendConstraint(self.getVarExtensionBoundaryBottom() == size[1])
		drawingSystem.appendConstraint(self.getVarOccupationBoundaryLeft() - self.getVarExtensionBoundaryLeft() == marginHorizontal)
		drawingSystem.appendConstraint(self.getVarOccupationBoundaryTop() - self.getVarExtensionBoundaryTop() == marginVertical)
		drawingSystem.appendConstraint(self.getVarExtensionBoundaryRight() - self.getVarOccupationBoundaryRight() == marginHorizontal)
		drawingSystem.appendConstraint(self.getVarExtensionBoundaryBottom() - self.getVarOccupationBoundaryBottom() == marginVertical)
		for component in self.components:
			component.appendConstraints(drawingSystem)

	def appendObjective(self, drawingSystem):
		super().appendObjective(drawingSystem)

		for component in self.components:
			component.appendObjective(drawingSystem)

