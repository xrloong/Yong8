from injector import inject

from .shape import ConstraintBoundaryShape

class LayoutConstraint:
	def __init__(self):
		self.alignToCenter = False

	def setAlignCenter(self, shape):
		self.targetShape = shape
		self.alignToCenter = True

	def isToAlignCenter(self):
		return self.alignToCenter

	def getTargetShape(self):
		return self.targetShape

class ConstraintComponent(ConstraintBoundaryShape):
	@inject
	def __init__(self):
		super().__init__()
		self.layoutConstraints = []

	def getComponentName(self):
		return "stroke_group"

	def setStrokes(self, strokes):
		self.strokes = strokes

	def appendLayoutConstraint(self, layoutConstraint):
		self.layoutConstraints.append(layoutConstraint)

	def appendConstraints(self, drawingSystem):
		super().appendConstraints(drawingSystem)
		for stroke in self.strokes:
			stroke.appendConstraints(drawingSystem)
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryLeft() <= stroke.getVarOccupationBoundaryLeft())
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryTop() <= stroke.getVarOccupationBoundaryTop())
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryRight() >= stroke.getVarOccupationBoundaryRight())
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryBottom() >= stroke.getVarOccupationBoundaryBottom())

		for layoutConstraint in self.layoutConstraints:
			targetShape = layoutConstraint.getTargetShape()
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryCenterX() == targetShape.getVarOccupationBoundaryCenterX())
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryCenterY() == targetShape.getVarOccupationBoundaryCenterY())

	def appendObjective(self, drawingSystem):
		super().appendObjective(drawingSystem)
		drawingSystem.appendObjective(-self.getVarOccupationBoundaryWidth()*2)
		drawingSystem.appendObjective(-self.getVarOccupationBoundaryHeight()*2)

		for stroke in self.strokes:
			stroke.appendObjective(drawingSystem)
			drawingSystem.appendObjective(stroke.getVarOccupationBoundaryWidth())
			drawingSystem.appendObjective(stroke.getVarOccupationBoundaryHeight())

