import abc
import uuid

from xrsolver.core.symbol import V
from xrsolver.core.symbol import One

from xrsolver.core.problem import Optimization
from xrsolver.core.problem import Problem

class ConstraintShape(object, metaclass=abc.ABCMeta):
	def __init__(self):
		super().__init__()
		self.compoundConstraints = []

	def addCompoundConstraint(self, compoundConstraint):
		self.compoundConstraints.append(compoundConstraint)

	def generateVariable(self, prefix, name, lb=None, ub=None) -> V:
		variableName = prefix+"."+name
		return V(variableName, lb, ub)

	def appendVariablesTo(self, problem):
		raise NotImplementedError('users must define appendVariablesTo() to use this base class')

	def appendConstraintsTo(self, problem):
		raise NotImplementedError('users must define appendConstraintsTo() to use this base class')

	def appendObjectivesTo(self, problem):
		raise NotImplementedError('users must define appendObjetivesTo() to use this base class')

	def appendSelfProblemTo(self, problem):
		self.appendVariablesTo(problem)
		self.appendConstraintsTo(problem)
		self.appendObjectivesTo(problem)

	def appendChildrenProblemTo(self, problem):
		pass

	def appendCompoundConstraintTo(self, problem):
		for compoundConstraint in self.compoundConstraints:
			problem.appendCompoundConstraint(compoundConstraint)

	def appendProblemTo(self, problem):
		self.appendSelfProblemTo(problem)
		self.appendChildrenProblemTo(problem)
		self.appendCompoundConstraintTo(problem)

	def generateProblem(self):
		problem = Problem()
		self.appendProblemTo(problem)
		return problem

class ConstraintRegion(ConstraintShape):
	def __init__(self):
		super().__init__()

		self.uuid = uuid.uuid4()

		componentPrefix = self.getComponentPrefix()

		self.boundaryLeft = self.generateVariable(componentPrefix, "boundary_left")
		self.boundaryTop = self.generateVariable(componentPrefix, "boundary_top")
		self.boundaryRight = self.generateVariable(componentPrefix, "boundary_right")
		self.boundaryBottom = self.generateVariable(componentPrefix, "boundary_bottom")
		self.boundaryWidth = self.generateVariable(componentPrefix, "boundary_width")
		self.boundaryHeight = self.generateVariable(componentPrefix, "boundary_height")
		self.boundaryCenterX = self.generateVariable(componentPrefix, "boundary_centerX")
		self.boundaryCenterY = self.generateVariable(componentPrefix, "boundary_centerY")

	def getId(self):
		return self.uuid

	def resolve(self, uuid):
		if self.uuid == uuid:
			return self
		else:
			return None

	def getComponentName(self):
		return "shape"

	def getComponentPrefix(self):
		return self.getComponentName()+"_"+str(self.uuid)

	def getVarBoundaryLeft(self):
		return self.boundaryLeft

	def getVarBoundaryTop(self):
		return self.boundaryTop

	def getVarBoundaryRight(self):
		return self.boundaryRight

	def getVarBoundaryBottom(self):
		return self.boundaryBottom

	def getVarBoundaryWidth(self):
		return self.boundaryWidth

	def getVarBoundaryHeight(self):
		return self.boundaryHeight

	def getVarBoundaryCenterX(self):
		return self.boundaryCenterX

	def getVarBoundaryCenterY(self):
		return self.boundaryCenterY


	def getVarBoundary(self):
		return (
			self.getVarBoundaryLeft(),
			self.getVarBoundaryTop(),
			self.getVarBoundaryRight(),
			self.getVarBoundaryBottom(),
			)

	def getBoundary(self):
		return (
			self.getVarBoundaryLeft().getValue(),
			self.getVarBoundaryTop().getValue(),
			self.getVarBoundaryRight().getValue(),
			self.getVarBoundaryBottom().getValue(),
			)

	def getBoundaryCenter(self):
		return (self.getVarBoundaryCenterX().getValue(),
			self.getVarBoundaryCenterY().getValue())

	def getSize(self):
		return (self.getVarBoundaryWidth().getValue(),
			self.getVarBoundaryHeight().getValue())


	def appendVariablesTo(self, problem):
		problem.addVariable(self.boundaryLeft)
		problem.addVariable(self.boundaryTop)
		problem.addVariable(self.boundaryRight)
		problem.addVariable(self.boundaryBottom)
		problem.addVariable(self.boundaryWidth)
		problem.addVariable(self.boundaryHeight)
		problem.addVariable(self.boundaryCenterX)
		problem.addVariable(self.boundaryCenterY)

	def appendConstraintsTo(self, problem):
		problem.appendConstraint(self.getVarBoundaryLeft() <= self.getVarBoundaryRight())
		problem.appendConstraint(self.getVarBoundaryTop() <= self.getVarBoundaryBottom())
		problem.appendConstraint(self.getVarBoundaryCenterX()*2 == self.getVarBoundaryLeft() + self.getVarBoundaryRight())
		problem.appendConstraint(self.getVarBoundaryCenterY()*2 == self.getVarBoundaryTop() + self.getVarBoundaryBottom())
		problem.appendConstraint(self.getVarBoundaryWidth() == self.getVarBoundaryRight() - self.getVarBoundaryLeft())
		problem.appendConstraint(self.getVarBoundaryHeight() == self.getVarBoundaryBottom() - self.getVarBoundaryTop())

	def appendObjectivesTo(self, problem):
		pass

class ConstraintBoundaryShape(ConstraintRegion):
	def __init__(self):
		super().__init__()

		componentPrefix = self.getComponentPrefix()

		self.minX = self.generateVariable(componentPrefix, "min_x")
		self.minY = self.generateVariable(componentPrefix, "min_y")
		self.maxX = self.generateVariable(componentPrefix, "max_x")
		self.maxY = self.generateVariable(componentPrefix, "max_y")

	def getComponentName(self):
		return "region"

	def getMinCandidatePoints(self):
		return ()

	def getMaxCandidatePoints(self):
		return ()

	def getVarMinX(self):
		return self.minX

	def getVarMinY(self):
		return self.minY

	def getVarMaxX(self):
		return self.maxX

	def getVarMaxY(self):
		return self.maxY

	def getVarOccupationBoundary(self):
		return (
			self.getVarMinX(),
			self.getVarMinY(),
			self.getVarMaxX(),
			self.getVarMaxY(),
			)

	def getVarOccupationTopLeft(self):
		return (self.getVarMinX(), self.getVarMinY())

	def getVarOccupationBottomRight(self):
		return (self.getVarMaxX(), self.getVarMaxY())

	def getMinX(self):
		return self.minX.getValue()

	def getMinY(self):
		return self.minY.getValue()

	def getMaxX(self):
		return self.maxX.getValue()

	def getMaxY(self):
		return self.maxY.getValue()

	def getOccupationBoundary(self):
		return (
			self.getMinX(),
			self.getMinY(),
			self.getMaxX(),
			self.getMaxY(),
			)

	def appendVariablesTo(self, problem):
		super().appendVariablesTo(problem)

		problem.addVariable(self.getVarMinX())
		problem.addVariable(self.getVarMinY())
		problem.addVariable(self.getVarMaxX())
		problem.addVariable(self.getVarMaxY())

	def appendConstraintsTo(self, problem):
		super().appendConstraintsTo(problem)

		problem.appendConstraint(self.getVarBoundaryLeft() == self.getVarMinX())
		problem.appendConstraint(self.getVarBoundaryTop() == self.getVarMinY())
		problem.appendConstraint(self.getVarBoundaryRight() == self.getVarMaxX())
		problem.appendConstraint(self.getVarBoundaryBottom() == self.getVarMaxY())

	def appendObjectivesTo(self, problem):
		super().appendObjectivesTo(problem)

		expMinX = One
		expMinY = One
		expMaxX = One
		expMaxY = One
		for point in self.getMinCandidatePoints():
			expMinX *= (point[0] - self.getVarMinX())
			expMinY *= (point[1] - self.getVarMinY())

		for point in self.getMaxCandidatePoints():
			expMaxX *= (self.getVarMaxX() - point[0])
			expMaxY *= (self.getVarMaxY() - point[1])

		problem.appendObjective(expMinX, Optimization.Minimize)
		problem.appendObjective(expMinY, Optimization.Minimize)
		problem.appendObjective(expMaxX, Optimization.Minimize)
		problem.appendObjective(expMaxY, Optimization.Minimize)


class PathParams:
	def __init__(self):
		self.layout_width_weight = 0
		self.layout_height_weight = 0

		self.range_weight_start_x = 0
		self.range_weight_end_x = 0
		self.range_weight_max_x = 0
		self.range_weight_start_y = 0
		self.range_weight_end_y = 1
		self.range_weight_max_y = 0

	def getWeights(self):
		return (self.layout_width_weight, self.layout_height_weight)

	def setWidthWeight(self, layout_width_weight):
		self.layout_width_weight = layout_width_weight

	def setHeightWeight(self, layout_height_weight):
		self.layout_height_weight = layout_height_weight

	def getRangeWeightStartX(self):
		return self.range_weight_start_x

	def getRangeWeightEndX(self):
		return self.range_weight_end_x

	def getRangeWeightMaxX(self):
		return self.range_weight_max_x

	def getRangeWeightStartY(self):
		return self.range_weight_start_y

	def getRangeWeightEndY(self):
		return self.range_weight_end_y

	def getRangeWeightMaxY(self):
		return self.range_weight_max_y

	def setRangeWeightX(self, weightStart, weightEnd, weightMax = 1):
		assert 0 <= weightStart <= weightMax
		assert 0 <= weightEnd <= weightMax
		self.range_weight_start_x = weightStart
		self.range_weight_end_x = weightEnd
		self.range_weight_max_x = weightMax

	def setRangeWeightY(self, weightStart, weightEnd, weightMax = 1):
		assert 0 <= weightStart <= weightMax
		assert 0 <= weightEnd <= weightMax
		self.range_weight_start_y = weightStart
		self.range_weight_end_y = weightEnd
		self.range_weight_max_y = weightMax

class ConstraintPath(ConstraintBoundaryShape):
	def __init__(self):
		super().__init__()

		self.pathParams = PathParams()

		componentPrefix = self.getComponentPrefix()
		self.startX = self.generateVariable(componentPrefix, "start_x")
		self.startY = self.generateVariable(componentPrefix, "start_y")
		self.endX = self.generateVariable(componentPrefix, "end_x")
		self.endY = self.generateVariable(componentPrefix, "end_y")

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "{1}-{2}, {0}".format(self.getBoundary(), self.getStartPoint(), self.getEndPoint())

	def getComponentName(self):
		return "path"

	def computeBoundary(self):
		return self.getBoundary()

	def setPathParams(self, pathParams):
		self.pathParams = pathParams

	def getPathParams(self):
		return self.pathParams


	def getVarStartX(self):
		return self.startX

	def getVarStartY(self):
		return self.startY

	def getVarEndX(self):
		return self.endX

	def getVarEndY(self):
		return self.endY

	def getVarStartPoint(self):
		return (self.getVarStartX(), self.getVarStartY())

	def getVarEndPoint(self):
		return (self.getVarEndX(), self.getVarEndY())

	def getStartPoint(self):
		return (self.getVarStartX().getValue(), self.getVarStartY().getValue())

	def getEndPoint(self):
		return (self.getVarEndX().getValue(), self.getVarEndY().getValue())


	def appendVariablesTo(self, problem):
		super().appendVariablesTo(problem)
		problem.addVariable(self.getVarStartX())
		problem.addVariable(self.getVarStartY())
		problem.addVariable(self.getVarEndX())
		problem.addVariable(self.getVarEndY())

	def appendConstraintsTo(self, problem):
		super().appendConstraintsTo(problem)

	def appendObjectivesTo(self, problem):
		super().appendObjectivesTo(problem)

