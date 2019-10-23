import abc
import uuid

from .problem import generateVariable
from .problem import Objective
from .problem import Optimization
from .problem import Problem

class ConstraintShape(object, metaclass=abc.ABCMeta):
	def __init__(self):
		super().__init__()
		self.compoundConstraints = []

	def draw(self, drawingSystem):
		raise NotImplementedError('users must define draw to use this base class')

	def addCompoundConstraint(self, compoundConstraint):
		self.compoundConstraints.append(compoundConstraint)

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

		self.boundaryLeft = generateVariable(componentPrefix, "boundary_left")
		self.boundaryTop = generateVariable(componentPrefix, "boundary_top")
		self.boundaryRight = generateVariable(componentPrefix, "boundary_right")
		self.boundaryBottom = generateVariable(componentPrefix, "boundary_bottom")
		self.boundaryWidth = generateVariable(componentPrefix, "boundary_width")
		self.boundaryHeight = generateVariable(componentPrefix, "boundary_height")
		self.boundaryCenterX = generateVariable(componentPrefix, "boundary_centerX")
		self.boundaryCenterY = generateVariable(componentPrefix, "boundary_centerY")

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
		self.appendConstraintsForBoundary(problem)

	def appendConstraintsForBoundary(self, problem):
		# boundary constraints
		problem.appendConstraint(self.getVarBoundaryLeft() <= self.getVarBoundaryRight())
		problem.appendConstraint(self.getVarBoundaryTop() <= self.getVarBoundaryBottom())
		problem.appendConstraint(self.getVarBoundaryCenterX()*2 == self.getVarBoundaryLeft() + self.getVarBoundaryRight())
		problem.appendConstraint(self.getVarBoundaryCenterY()*2 == self.getVarBoundaryTop() + self.getVarBoundaryBottom())
		problem.appendConstraint(self.getVarBoundaryWidth() == self.getVarBoundaryRight() - self.getVarBoundaryLeft())
		problem.appendConstraint(self.getVarBoundaryHeight() == self.getVarBoundaryBottom() - self.getVarBoundaryTop())

	def appendConstraintsWithBoundary(self, problem, boundary):
		left, top, right, bottom = boundary
		problem.appendConstraint(self.getVarBoundaryLeft() == left)
		problem.appendConstraint(self.getVarBoundaryTop() == top)
		problem.appendConstraint(self.getVarBoundaryRight() == right)
		problem.appendConstraint(self.getVarBoundaryBottom() == bottom)

	def appendConstraintsWithSizeCenter(self, problem, size, center):
		width, height = size
		centerX, centerY = center
		problem.appendConstraint(self.getVarBoundaryWidth() == width)
		problem.appendConstraint(self.getVarBoundaryHeight() == height)
		problem.appendConstraint(self.getVarBoundaryCenterX() == centerX)
		problem.appendConstraint(self.getVarBoundaryCenterY() == centerY)

	def appendObjectivesTo(self, problem):
		pass

class ConstraintBoundaryShape(ConstraintRegion):
	def __init__(self):
		super().__init__()

		componentPrefix = self.getComponentPrefix()

		self.minX = generateVariable(componentPrefix, "min_x")
		self.minY = generateVariable(componentPrefix, "min_y")
		self.maxX = generateVariable(componentPrefix, "max_x")
		self.maxY = generateVariable(componentPrefix, "max_y")

	def getComponentName(self):
		return "region"

	def getVarMinX(self):
		return self.minX

	def getVarMinY(self):
		return self.minY

	def getVarMaxX(self):
		return self.maxX

	def getVarMaxY(self):
		return self.maxY

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

	def setWeights(self, width_weight, height_weight):
		self.layout_width_weight = width_weight
		self.layout_height_weight = height_weight

	def getWeights(self):
		return (self.layout_width_weight, self.layout_height_weight)

	def getWidthWeight(self):
		return self.layout_width_weight

	def getHeightWeight(self):
		return self.layout_height_weight

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

	def setRangeWeightStartX(self, weight):
		self.range_weight_start_x = weight

	def setRangeWeightEndX(self, weight):
		self.range_weight_end_x = weight

	def setRangeWeightMaxX(self, weight):
		self.range_weight_max_x = weight

	def setRangeWeightX(self, weightStart, weightEnd, weightMax = 1):
		assert 0 <= weightStart <= weightMax
		assert 0 <= weightEnd <= weightMax
		self.range_weight_start_x = weightStart
		self.range_weight_end_x = weightEnd
		self.range_weight_max_x = weightMax

	def setRangeWeightStartY(self, weight):
		self.range_weight_start_y = weight

	def setRangeWeightEndY(self, weight):
		self.range_weight_end_y = weight

	def setRangeWeightMaxY(self, weight):
		self.range_weight_max_y = weight

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
		self.startX = generateVariable(componentPrefix, "start_x")
		self.startY = generateVariable(componentPrefix, "start_y")
		self.endX = generateVariable(componentPrefix, "end_x")
		self.endY = generateVariable(componentPrefix, "end_y")

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "{1}-{2}, {0}".format(self.getBoundary(), self.getStartPoint(), self.getEndPoint())

	def getComponentName(self):
		return "path"

	def draw(self, drawingSystem):
		pass

	def computeBoundary(self):
		return self.getBoundary()

	def setPathParams(self, pathParams):
		self.pathParams = pathParams

	def getPathParams(self):
		return self.pathParams

	def getStartPoint(self):
		return (self.startX.getValue(),
			self.startY.getValue())

	def getEndPoint(self):
		return (self.endX.getValue(),
			self.endY.getValue())

	def getVarStartX(self):
		return self.startX

	def getVarStartY(self):
		return self.startY

	def getVarEndX(self):
		return self.endX

	def getVarEndY(self):
		return self.endY

	def appendVariablesTo(self, problem):
		super().appendVariablesTo(problem)
		problem.addVariable(self.startX)
		problem.addVariable(self.startY)
		problem.addVariable(self.endX)
		problem.addVariable(self.endY)

	def appendConstraintsForPoints(self, problem):
		problem.appendConstraint(self.getVarBoundaryLeft() <= self.startX)
		problem.appendConstraint(self.getVarBoundaryLeft() <= self.endX)

		problem.appendConstraint(self.getVarBoundaryTop() <= self.startY)
		problem.appendConstraint(self.getVarBoundaryTop() <= self.endY)

		problem.appendConstraint(self.getVarBoundaryRight() >= self.startX)
		problem.appendConstraint(self.getVarBoundaryRight() >= self.endX)

		problem.appendConstraint(self.getVarBoundaryBottom() >= self.startY)
		problem.appendConstraint(self.getVarBoundaryBottom() >= self.endY)

	def appendConstraintsTo(self, problem):
		super().appendConstraintsTo(problem)
		self.appendConstraintsForPoints(problem)

		problem.appendConstraint(self.getVarMinX() <= self.getVarStartX())
		problem.appendConstraint(self.getVarMinX() <= self.getVarEndX())
		problem.appendConstraint(self.getVarMinY() <= self.getVarStartY())
		problem.appendConstraint(self.getVarMinY() <= self.getVarEndY())

		problem.appendConstraint(self.getVarMaxX() >= self.getVarStartX())
		problem.appendConstraint(self.getVarMaxX() >= self.getVarEndX())
		problem.appendConstraint(self.getVarMaxY() >= self.getVarStartY())
		problem.appendConstraint(self.getVarMaxY() >= self.getVarEndY())

	def appendObjectivesTo(self, problem):
		super().appendObjectivesTo(problem)

		problem.appendObjective(Objective(self.getVarStartX() - self.getVarMinX(), Optimization.Minimize))
		problem.appendObjective(Objective(self.getVarEndX() - self.getVarMinX(), Optimization.Minimize))
		problem.appendObjective(Objective(self.getVarStartY() - self.getVarMinY(), Optimization.Minimize))
		problem.appendObjective(Objective(self.getVarEndY() - self.getVarMinY(), Optimization.Minimize))

		problem.appendObjective(Objective(self.getVarMaxX() - self.getVarStartX(), Optimization.Minimize))
		problem.appendObjective(Objective(self.getVarMaxX() - self.getVarEndX(), Optimization.Minimize))
		problem.appendObjective(Objective(self.getVarMaxY() - self.getVarStartY(), Optimization.Minimize))
		problem.appendObjective(Objective(self.getVarMaxY() - self.getVarEndY(), Optimization.Minimize))

	def resolvePointStart(self):
		return (self.getVarStartX(), self.getVarStartY())

	def resolvePointEnd(self):
		return (self.getVarEndX(), self.getVarEndY())

