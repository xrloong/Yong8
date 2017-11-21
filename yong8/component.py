from injector import inject
from enum import Enum

from .shape import ConstraintBoundaryShape

class ConstraintType(Enum):
	Non = 0
	Row = 1
	Objective = 2
	Maximize = 3
	Minimize = 4
	AlignToCenter = 5

class LayoutConstraint:
	def __init__(self):
		self.type = ConstraintType.Non

	def setAsRow(self, constraint):
		self.type = ConstraintType.Row
		self.constraint = constraint

	def setAsObjective(self, objective):
		self.type = ConstraintType.Objective
		self.objective = objective

	def setAsMaximize(self, objective):
		self.type = ConstraintType.Maximize
		self.objective = objective

	def setAsMinimize(self, objective):
		self.type = ConstraintType.Minimize
		self.objective = objective

	def setAlignCenter(self, shape):
		self.type = ConstraintType.AlignToCenter
		self.targetShape = shape

	def isRow(self):
		return self.type == ConstraintType.Row

	def isObjective(self):
		return self.type == ConstraintType.Objective

	def isMaximize(self):
		return self.type == ConstraintType.Maximize

	def isMinimize(self):
		return self.type == ConstraintType.Minimize

	def isToAlignCenter(self):
		return self.type == ConstraintType.AlignToCenter

	def getTargetShape(self):
		return self.targetShape

	def getRowConstraint(self):
		return self.constraint

	def getObjective(self):
		return self.objective

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
			self.appendContraintFromLayoutConstraint(drawingSystem, layoutConstraint)

	def appendContraintFromLayoutConstraint(self, drawingSystem, layoutConstraint):
		if layoutConstraint.isToAlignCenter():
			targetShape = layoutConstraint.getTargetShape()
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryCenterX() == targetShape.getVarOccupationBoundaryCenterX())
			drawingSystem.appendConstraint(self.getVarOccupationBoundaryCenterY() == targetShape.getVarOccupationBoundaryCenterY())
		if layoutConstraint.isRow():
			drawingSystem.appendConstraint(layoutConstraint.getRowConstraint())


	def appendObjective(self, drawingSystem):
		super().appendObjective(drawingSystem)
		for layoutConstraint in self.layoutConstraints:
			self.appendObjectiveFromLayoutConstraint(drawingSystem, layoutConstraint)

	def appendObjectiveFromLayoutConstraint(self, drawingSystem, layoutConstraint):
		if layoutConstraint.isObjective():
			drawingSystem.appendObjective(layoutConstraint.getObjective())
		if layoutConstraint.isMaximize():
			drawingSystem.appendObjective(layoutConstraint.getObjective())
		if layoutConstraint.isMinimize():
			drawingSystem.appendObjective(layoutConstraint.getObjective()*-1)
