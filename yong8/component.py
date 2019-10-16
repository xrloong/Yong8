from injector import inject
from enum import Enum

from .constants import Optimization
from .shape import ConstraintBoundaryShape

class ConstraintType(Enum):
	Non = 0
	Row = 1
	Objective = 2
	Maximize = 3
	Minimize = 4
	AlignToCenter = 5
	PointMatchPoint = 6

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

	def setAsAlignCenter(self, shape):
		self.type = ConstraintType.AlignToCenter
		self.targetShape = shape

	def setAsPointMatchPoint(self, point1, point2):
		self.type = ConstraintType.PointMatchPoint
		self.pointMatchPoint = (point1, point2)

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

	def isPointMatchPoint(self):
		return self.type == ConstraintType.PointMatchPoint

	def getTargetShape(self):
		return self.targetShape

	def getRowConstraint(self):
		return self.constraint

	def getObjective(self):
		return self.objective

	def getPointMatchPoint(self):
		return self.pointMatchPoint

class ConstraintComponent(ConstraintBoundaryShape):
	@inject
	def __init__(self):
		super().__init__()
		self.layoutConstraints = []

	def getComponentName(self):
		return "stroke_group"

	def resolve(self, uuid):
		for stroke in self.strokes:
			s = stroke.resolve(uuid)
			if s != None:
				return s
		return None

	def setStrokes(self, strokes):
		self.strokes = strokes

	def getStrokes(self):
		return self.strokes

	def appendVariables(self, problem):
		super().appendVariables(problem)
		for stroke in self.getStrokes():
			stroke.appendVariables(problem)

	def appendLayoutConstraint(self, layoutConstraint):
		self.layoutConstraints.append(layoutConstraint)

	def appendConstraints(self, problem):
		super().appendConstraints(problem)
		for stroke in self.strokes:
			stroke.appendConstraints(problem)
			problem.appendConstraint(self.getVarOccupationBoundaryLeft() <= stroke.getVarOccupationBoundaryLeft())
			problem.appendConstraint(self.getVarOccupationBoundaryTop() <= stroke.getVarOccupationBoundaryTop())
			problem.appendConstraint(self.getVarOccupationBoundaryRight() >= stroke.getVarOccupationBoundaryRight())
			problem.appendConstraint(self.getVarOccupationBoundaryBottom() >= stroke.getVarOccupationBoundaryBottom())

		for layoutConstraint in self.layoutConstraints:
			self.appendContraintFromLayoutConstraint(problem, layoutConstraint)

	def appendContraintFromLayoutConstraint(self, problem, layoutConstraint):
		if layoutConstraint.isToAlignCenter():
			targetShape = layoutConstraint.getTargetShape()
			problem.appendConstraint(self.getVarOccupationBoundaryCenterX() == targetShape.getVarOccupationBoundaryCenterX())
			problem.appendConstraint(self.getVarOccupationBoundaryCenterY() == targetShape.getVarOccupationBoundaryCenterY())
		if layoutConstraint.isRow():
			problem.appendConstraint(layoutConstraint.getRowConstraint())
		if layoutConstraint.isPointMatchPoint():
			pointMatchPoint = layoutConstraint.getPointMatchPoint()
			point1, point2 = pointMatchPoint
			problem.appendConstraint(point1[0] == point2[0])
			problem.appendConstraint(point1[1] == point2[1])


	def appendObjective(self, problem):
		super().appendObjective(problem)
		for layoutConstraint in self.layoutConstraints:
			self.appendObjectiveFromLayoutConstraint(problem, layoutConstraint)

	def appendObjectiveFromLayoutConstraint(self, problem, layoutConstraint):
		if layoutConstraint.isObjective():
			problem.appendObjective(layoutConstraint.getObjective(), Optimization.Maximize)
		if layoutConstraint.isMaximize():
			problem.appendObjective(layoutConstraint.getObjective(), Optimization.Maximize)
		if layoutConstraint.isMinimize():
			problem.appendObjective(layoutConstraint.getObjective(), Optimization.Minimize)

