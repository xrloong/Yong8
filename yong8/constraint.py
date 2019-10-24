import abc
import uuid
from enum import Enum

class CompoundConstraint(object, metaclass=abc.ABCMeta):
	def getVariables(self):
		raise NotImplementedError('users must define getVariables() to use this base class')

	def getConstraints(self):
		raise NotImplementedError('users must define getConstraints() to use this base class')

	def getObjectives(self):
		raise NotImplementedError('users must define getObjectives() to use this base class')


class IntersectionPos(Enum):
	Unknown = 0
	BeforeStart = 1
	Start = 2
	BetweenStartEnd = 3
	End = 4
	AfterEnd = 5

class SegmentIntersectionConstraint(CompoundConstraint):
	def __init__(self, segment1, segment2, intersectionPos1 = IntersectionPos.BetweenStartEnd, intersectionPos2 = IntersectionPos.BetweenStartEnd):
		self.seg1 = segment1
		self.seg2 = segment2

		self.uuid = uuid.uuid4()

		from .problem import generateVariable

		intersectionPrefix = "intersection-{0}-{1}".format(segment1.getId(), segment2.getId())
		self.intersectionX = generateVariable(intersectionPrefix, "intersection_x")
		self.intersectionY = generateVariable(intersectionPrefix, "intersection_y")
		self.t1 = generateVariable(intersectionPrefix, "t1")
		self.t2 = generateVariable(intersectionPrefix, "t2")
		self.intersections = (self.t1, self.t2)
		self.pos1 = intersectionPos1
		self.pos2 = intersectionPos2

	def getVariables(self):
		return (self.intersectionX, self.intersectionY, self.t1, self.t2)

	def getConstraints(self):
		point1 = self.seg1.getPointAt(self.t1)
		point2 = self.seg2.getPointAt(self.t2)

		pos1 = self.pos1
		pos2 = self.pos2
		t1 = self.t1
		t2 = self.t2
		constraintList = []
		if pos1 == IntersectionPos.BeforeStart:
			constraintList.append(t1 < 0)
		elif pos1 == IntersectionPos.Start:
			constraintList.append(t1 == 0)
		elif pos1 == IntersectionPos.BetweenStartEnd:
			constraintList.append(0 < t1)
			constraintList.append(t1 < 1)
		elif pos1 == IntersectionPos.End:
			constraintList.append(t1 == 1)
		elif pos1 == IntersectionPos.AfterEnd:
			constraintList.append(t1 > 1)

		if pos2 == IntersectionPos.BeforeStart:
			constraintList.append(t2 < 0)
		elif pos2 == IntersectionPos.Start:
			constraintList.append(t2 == 0)
		elif pos2 == IntersectionPos.BetweenStartEnd:
			constraintList.append(0 < t2)
			constraintList.append(t2 < 1)
		elif pos2 == IntersectionPos.End:
			constraintList.append(t2 == 1)
		elif pos2 == IntersectionPos.AfterEnd:
			constraintList.append(t2 > 1)

		return (
			0 <= self.t1, self.t1 <= 1,
			0 <= self.t2, self.t2 <= 1,

			point1[0] == self.intersectionX,
			point1[1] == self.intersectionY,
			point2[0] == self.intersectionX,
			point2[1] == self.intersectionY,
			) + tuple(constraintList)

	def getObjectives(self):
		return ()


class PointMatchingConstraint(CompoundConstraint):
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2

	def getVariables(self):
		return ()

	def getConstraints(self):
		point1 = self.point1
		point2 = self.point2
		return (
			point1[0] == point2[0],
			point1[1] == point2[1],
			)

	def getObjectives(self):
		return ()

class AlignCenterConstraint(CompoundConstraint):
	def __init__(self, shape1, shape2):
		self.shape1 = shape1
		self.shape2 = shape2

	def getVariables(self):
		return ()

	def getConstraints(self):
		shape1 = self.shape1
		shape2 = self.shape2
		return (
			shape1.getVarBoundaryCenterX() == shape2.getVarBoundaryCenterX(),
			shape1.getVarBoundaryCenterY() == shape2.getVarBoundaryCenterY()
			)

	def getObjectives(self):
		return ()

class BoundaryConstraint(CompoundConstraint):
	def __init__(self, shape, boundary):
		self.shape = shape
		self.boundary = boundary

	def getVariables(self):
		return ()

	def getConstraints(self):
		shape = self.shape
		left, top, right, bottom = self.boundary
		return (
			shape.getVarBoundaryLeft() == left,
			shape.getVarBoundaryTop() == top,
			shape.getVarBoundaryRight() == right,
			shape.getVarBoundaryBottom() == bottom
			)

	def getObjectives(self):
		return ()

