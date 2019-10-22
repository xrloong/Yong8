from enum import Enum

from .constants import Optimization
from .problem import generateVariable
from .problem import Objective
from .shape import ConstraintBoundaryShape

class ConstraintType(Enum):
	Non = 0
	Row = 1
	AlignToCenter = 5

class LayoutConstraint:
	def __init__(self):
		self.type = ConstraintType.Non

	def setAsRow(self, constraint):
		self.type = ConstraintType.Row
		self.constraint = constraint

	def setAsAlignCenter(self, shape):
		self.type = ConstraintType.AlignToCenter
		self.targetShape = shape

	def isRow(self):
		return self.type == ConstraintType.Row

	def isToAlignCenter(self):
		return self.type == ConstraintType.AlignToCenter

	def getTargetShape(self):
		return self.targetShape

	def getRowConstraint(self):
		return self.constraint

	def getObjective(self):
		return self.objective

	def getSegments(self):
		return self.segments

class ConstraintComponent(ConstraintBoundaryShape):
	def __init__(self, strokes):
		super().__init__()

		self.strokes = strokes
		self.layoutConstraints = []
		self.compoundConstraints = []

	def dump(self):
		for stroke in self.strokes:
			print("stroke:", stroke)
			print("start point:", stroke.getStartPoint())
			print("end point:", stroke.getEndPoint())
			print()

	def getComponentName(self):
		return "stroke_group"

	def resolve(self, uuid):
		for stroke in self.strokes:
			s = stroke.resolve(uuid)
			if s != None:
				return s
		return None

	def getStrokes(self):
		return self.strokes

	def appendLayoutConstraint(self, layoutConstraint):
		self.layoutConstraints.append(layoutConstraint)

	def appendCompoundConstraint(self, compoundConstraint):
		self.compoundConstraints.append(compoundConstraint)

	def appendChildrenProblemTo(self, problem):
		super().appendChildrenProblemTo(problem)

		for stroke in self.getStrokes():
			subProblem = stroke.generateProblem()
			problem.appendProblem(subProblem)

			problem.appendConstraint(self.getVarBoundaryLeft() <= stroke.getVarBoundaryLeft())
			problem.appendConstraint(self.getVarBoundaryTop() <= stroke.getVarBoundaryTop())
			problem.appendConstraint(self.getVarBoundaryRight() >= stroke.getVarBoundaryRight())
			problem.appendConstraint(self.getVarBoundaryBottom() >= stroke.getVarBoundaryBottom())

		self.appendLayoutContraintsProblemTo(problem)

		for compoundConstraint in self.compoundConstraints:
			problem.appendCompoundConstraint(compoundConstraint)

	def appendLayoutContraintsProblemTo(self, problem):
		for layoutConstraint in self.layoutConstraints:
			self.appendContraintFromLayoutConstraint(problem, layoutConstraint)

	def appendContraintFromLayoutConstraint(self, problem, layoutConstraint):
		if layoutConstraint.isToAlignCenter():
			targetShape = layoutConstraint.getTargetShape()
			problem.appendConstraint(self.getVarBoundaryCenterX() == targetShape.getVarBoundaryCenterX())
			problem.appendConstraint(self.getVarBoundaryCenterY() == targetShape.getVarBoundaryCenterY())
		if layoutConstraint.isRow():
			problem.appendConstraint(layoutConstraint.getRowConstraint())

