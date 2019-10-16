from injector import inject
from enum import Enum

from .constants import Optimization
from .problem import Objective
from .shape import ConstraintBoundaryShape
from .stroke import generateVariable

class IntersectionPos(Enum):
	Unknown = 0
	BeforeStart = 1
	Start = 2
	BetweenStartEnd = 3
	End = 4
	AfterEnd = 5

class ConstraintType(Enum):
	Non = 0
	Row = 1
	Objective = 2
	Maximize = 3
	Minimize = 4
	AlignToCenter = 5
	PointMatchPoint = 6
	SegmentsIntersection = 7

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

	def setAsSegmentsIntersection(self, segment1, segment2, intersectionPos1 = IntersectionPos.BetweenStartEnd, intersectionPos2 = IntersectionPos.BetweenStartEnd):
		self.type = ConstraintType.SegmentsIntersection
		self.segments = (segment1, segment2)
		self.intersectionPos = (intersectionPos1, intersectionPos2)
		intersection_prfix = "intersection-{0}-{1}".format(segment1.getId(), segment2.getId())
		t1 = generateVariable(intersection_prfix, "t1")
		t2 = generateVariable(intersection_prfix, "t2")
		self.intersections = (t1, t2)

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

	def isSegmentsIntersection(self):
		return self.type == ConstraintType.SegmentsIntersection

	def getTargetShape(self):
		return self.targetShape

	def getRowConstraint(self):
		return self.constraint

	def getObjective(self):
		return self.objective

	def getPointMatchPoint(self):
		return self.pointMatchPoint

	def getSegments(self):
		return self.segments

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

		if layoutConstraint.isSegmentsIntersection():
			segment1, segment2 = layoutConstraint.getSegments()
			(t1, t2) = layoutConstraint.intersections
			(pos1, pos2) = layoutConstraint.intersectionPos
			point1 = segment1.getPointAt(t1)
			point2 = segment2.getPointAt(t2)
			problem.addVariable(t1)
			problem.addVariable(t2)

			problem.appendConstraint(point1[0] == point2[0])
			problem.appendConstraint(point1[1] == point2[1])

			if pos1 == IntersectionPos.BeforeStart:
				problem.appendConstraint(t1 < 0)
			elif pos1 == IntersectionPos.Start:
				problem.appendConstraint(t1 == 0)
			elif pos1 == IntersectionPos.BetweenStartEnd:
				problem.appendConstraint(0 < t1)
				problem.appendConstraint(t1 < 1)
			elif pos1 == IntersectionPos.End:
				problem.appendConstraint(t1 == 1)
			elif pos1 == IntersectionPos.AfterEnd:
				problem.appendConstraint(t1 > 1)

			if pos2 == IntersectionPos.BeforeStart:
				problem.appendConstraint(t2 < 0)
			elif pos2 == IntersectionPos.Start:
				problem.appendConstraint(t2 == 0)
			elif pos2 == IntersectionPos.BetweenStartEnd:
				problem.appendConstraint(0 < t2)
				problem.appendConstraint(t2 < 1)
			elif pos2 == IntersectionPos.End:
				problem.appendConstraint(t2 == 1)
			elif pos2 == IntersectionPos.AfterEnd:
				problem.appendConstraint(t2 > 1)


	def appendObjective(self, problem):
		super().appendObjective(problem)
		for layoutConstraint in self.layoutConstraints:
			self.appendObjectiveFromLayoutConstraint(problem, layoutConstraint)

	def appendObjectiveFromLayoutConstraint(self, problem, layoutConstraint):
		if layoutConstraint.isObjective():
			problem.appendObjective(Objective(layoutConstraint.getObjective(), Optimization.Maximize))
		if layoutConstraint.isMaximize():
			problem.appendObjective(Objective(layoutConstraint.getObjective(), Optimization.Maximize))
		if layoutConstraint.isMinimize():
			problem.appendObjective(Objective(layoutConstraint.getObjective(), Optimization.Minimize))

