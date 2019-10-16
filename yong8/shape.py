import abc
import uuid

from injector import inject

from .drawing import DrawingGlyphPolicy
from .problem import Objective
from .problem import Problem
from .symbol import generateVariable

class ConstraintShape(object, metaclass=abc.ABCMeta):
	@inject
	def __init__(self):
		super().__init__()

	def draw(self, drawingSystem):
		raise NotImplementedError('users must define draw to use this base class')

	def appendVariables(self, problem):
		raise NotImplementedError('users must define appendVariables to use this base class')

	def appendConstraints(self, problem):
		raise NotImplementedError('users must define appendConstraints to use this base class')

	def appendObjective(self, problem):
		raise NotImplementedError('users must define appendObjetive to use this base class')

	def appendSelfProblemTo(self, problem):
		self.appendVariables(problem)
		self.appendConstraints(problem)
		self.appendObjective(problem)

	def appendChildrenProblemTo(self, problem):
		pass

	def appendProblemTo(self, problem):
		self.appendSelfProblemTo(problem)
		self.appendChildrenProblemTo(problem)

	def generateProblem(self, drawingPolicyPolicy: DrawingGlyphPolicy):
		problem = Problem(drawingPolicyPolicy)
		self.appendProblemTo(problem)
		return problem

class ConstraintBoundaryShape(ConstraintShape):
	@inject
	def __init__(self):
		super().__init__()

		self.uuid = uuid.uuid4()

		componentPrefix = self.getComponentPrefix()
		self.occupationBoundaryLeft = generateVariable(componentPrefix, "occupation_boundary_left")
		self.occupationBoundaryTop = generateVariable(componentPrefix, "occupation_boundary_top")
		self.occupationBoundaryRight = generateVariable(componentPrefix, "occupation_boundary_right")
		self.occupationBoundaryBottom = generateVariable(componentPrefix, "occupation_boundary_bottom")
		self.occupationBoundaryWidth = generateVariable(componentPrefix, "occupation_boundary_width")
		self.occupationBoundaryHeight = generateVariable(componentPrefix, "occupation_boundary_height")
		self.occupationBoundaryCenterX = generateVariable(componentPrefix, "occupation_boundary_centerX")
		self.occupationBoundaryCenterY = generateVariable(componentPrefix, "occupation_boundary_centerY")

		self.extensionBoundaryLeft = generateVariable(componentPrefix, "extension_boundary_left")
		self.extensionBoundaryTop = generateVariable(componentPrefix, "extension_boundary_top")
		self.extensionBoundaryRight = generateVariable(componentPrefix, "extension_boundary_right")
		self.extensionBoundaryBottom = generateVariable(componentPrefix, "extension_boundary_bottom")
		self.extensionBoundaryWidth = generateVariable(componentPrefix, "extension_boundary_width")
		self.extensionBoundaryHeight = generateVariable(componentPrefix, "extension_boundary_height")
		self.extensionBoundaryCenterX = generateVariable(componentPrefix, "extension_boundary_centerX")
		self.extensionBoundaryCenterY = generateVariable(componentPrefix, "extension_boundary_centerY")

		self.expMinX = self.occupationBoundaryLeft
		self.expMinY = self.occupationBoundaryTop
		self.expMaxX = self.occupationBoundaryRight
		self.expMaxY = self.occupationBoundaryBottom

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
		return self.getVarOccupationBoundaryLeft()

	def getVarBoundaryTop(self):
		return self.getVarOccupationBoundaryTop()

	def getVarBoundaryRight(self):
		return self.getVarOccupationBoundaryRight()

	def getVarBoundaryBottom(self):
		return self.getVarOccupationBoundaryBottom()

	def getVarBoundaryWidth(self):
		return self.getVarOccupationBoundaryWidth()

	def getVarBoundaryHeight(self):
		return self.getVarOccupationBoundaryHeight()

	def getVarBoundaryCenterX(self):
		return self.getVarOccupationBoundaryCenterX()

	def getVarBoundaryCenterY(self):
		return self.getVarOccupationBoundaryCenterY()


	def getVarOccupationBoundaryLeft(self):
		return self.occupationBoundaryLeft

	def getVarOccupationBoundaryTop(self):
		return self.occupationBoundaryTop

	def getVarOccupationBoundaryRight(self):
		return self.occupationBoundaryRight

	def getVarOccupationBoundaryBottom(self):
		return self.occupationBoundaryBottom

	def getVarOccupationBoundaryWidth(self):
		return self.occupationBoundaryWidth

	def getVarOccupationBoundaryHeight(self):
		return self.occupationBoundaryHeight

	def getVarOccupationBoundaryCenterX(self):
		return self.occupationBoundaryCenterX

	def getVarOccupationBoundaryCenterY(self):
		return self.occupationBoundaryCenterY


	def getVarExtensionBoundaryLeft(self):
		return self.extensionBoundaryLeft

	def getVarExtensionBoundaryTop(self):
		return self.extensionBoundaryTop

	def getVarExtensionBoundaryRight(self):
		return self.extensionBoundaryRight

	def getVarExtensionBoundaryBottom(self):
		return self.extensionBoundaryBottom

	def getVarExtensionBoundaryWidth(self):
		return self.extensionBoundaryWidth

	def getVarExtensionBoundaryHeight(self):
		return self.extensionBoundaryHeight

	def getVarExtensionBoundaryCenterX(self):
		return self.extensionBoundaryCenterX

	def getVarExtensionBoundaryCenterY(self):
		return self.extensionBoundaryCenterY

	def getOccupationBoundary(self):
		return (
			self.getVarOccupationBoundaryLeft().getValue(),
			self.getVarOccupationBoundaryTop().getValue(),
			self.getVarOccupationBoundaryRight().getValue(),
			self.getVarOccupationBoundaryBottom().getValue(),
			)

	def getExtensionBoundary(self):
		return (
			self.getVarExtensionBoundaryLeft().getValue(),
			self.getVarExtensionBoundaryTop().getValue(),
			self.getVarExtensionBoundaryRight().getValue(),
			self.getVarExtensionBoundaryBottom().getValue(),
			)

	def getOccupationBoundaryCenter(self):
		return (self.getVarOccupationBoundaryCenterX().getValue(),
			self.getVarOccupationBoundaryCenterY().getValue())

	def getExtensionBoundaryCenter(self):
		return (self.getVarExtensionBoundaryCenterX().getValue(),
			self.getVarExtensionBoundaryCenterY().getValue())

	def getOccupationSize(self):
		return (self.getVarOccupationBoundaryWidth().getValue(),
			self.getVarOccupationBoundaryHeight().getValue())

	def getExtensionSize(self):
		return (self.getVarExtensionBoundaryWidth().getValue(),
			self.getVarExtensionBoundaryHeight().getValue())


	def getExpMinX(self):
		return self.expMinX

	def getExpMinY(self):
		return self.expMinY

	def getExpMaxX(self):
		return self.expMaxX

	def getExpMaxY(self):
		return self.expMaxY


	def getBoundary(self):
		return self.getOccupationBoundary()

	def getBoundaryCenter(self):
		return self.getOccupationBoundaryCenter()

	def getSize(self):
		return self.getOccupationSize()


	def appendVariables(self, problem):
		problem.addVariable(self.occupationBoundaryLeft)
		problem.addVariable(self.occupationBoundaryTop)
		problem.addVariable(self.occupationBoundaryRight)
		problem.addVariable(self.occupationBoundaryBottom)
		problem.addVariable(self.occupationBoundaryWidth)
		problem.addVariable(self.occupationBoundaryHeight)
		problem.addVariable(self.occupationBoundaryCenterX)
		problem.addVariable(self.occupationBoundaryCenterY)

		problem.addVariable(self.extensionBoundaryLeft)
		problem.addVariable(self.extensionBoundaryTop)
		problem.addVariable(self.extensionBoundaryRight)
		problem.addVariable(self.extensionBoundaryBottom)
		problem.addVariable(self.extensionBoundaryWidth)
		problem.addVariable(self.extensionBoundaryHeight)
		problem.addVariable(self.extensionBoundaryCenterX)
		problem.addVariable(self.extensionBoundaryCenterY)

	def appendConstraints(self, problem):
		self.appendConstraintsForBoundary(problem)

	def appendConstraintsForBoundary(self, problem):
		# occupation constraints
		problem.appendConstraint(self.getVarOccupationBoundaryLeft() <= self.getVarOccupationBoundaryRight())
		problem.appendConstraint(self.getVarOccupationBoundaryTop() <= self.getVarOccupationBoundaryBottom())
		problem.appendConstraint(self.getVarOccupationBoundaryCenterX()*2 == self.getVarOccupationBoundaryLeft() + self.getVarOccupationBoundaryRight())
		problem.appendConstraint(self.getVarOccupationBoundaryCenterY()*2 == self.getVarOccupationBoundaryTop() + self.getVarOccupationBoundaryBottom())
		problem.appendConstraint(self.getVarOccupationBoundaryWidth() == self.getVarOccupationBoundaryRight() - self.getVarOccupationBoundaryLeft())
		problem.appendConstraint(self.getVarOccupationBoundaryHeight() == self.getVarOccupationBoundaryBottom() - self.getVarOccupationBoundaryTop())

		# extension constraints
		problem.appendConstraint(self.getVarExtensionBoundaryLeft() <= self.getVarExtensionBoundaryRight())
		problem.appendConstraint(self.getVarExtensionBoundaryTop() <= self.getVarExtensionBoundaryBottom())
		problem.appendConstraint(self.getVarExtensionBoundaryCenterX()*2 == self.getVarExtensionBoundaryLeft() + self.getVarExtensionBoundaryRight())
		problem.appendConstraint(self.getVarExtensionBoundaryCenterY()*2 == self.getVarExtensionBoundaryTop() + self.getVarExtensionBoundaryBottom())
		problem.appendConstraint(self.getVarExtensionBoundaryWidth() == self.getVarExtensionBoundaryRight() - self.getVarExtensionBoundaryLeft())
		problem.appendConstraint(self.getVarExtensionBoundaryHeight() == self.getVarExtensionBoundaryBottom() - self.getVarExtensionBoundaryTop())

		problem.appendConstraint(self.getVarExtensionBoundaryLeft() <= self.getVarOccupationBoundaryLeft())
		problem.appendConstraint(self.getVarExtensionBoundaryTop() <= self.getVarOccupationBoundaryTop())
		problem.appendConstraint(self.getVarExtensionBoundaryRight() >= self.getVarOccupationBoundaryRight())
		problem.appendConstraint(self.getVarExtensionBoundaryBottom() >= self.getVarOccupationBoundaryBottom())

		# make occupation to match the shape
		problem.appendConstraint(self.getVarOccupationBoundaryLeft() == self.getExpMinX())
		problem.appendConstraint(self.getVarOccupationBoundaryTop() == self.getExpMinY())
		problem.appendConstraint(self.getVarOccupationBoundaryRight() == self.getExpMaxX())
		problem.appendConstraint(self.getVarOccupationBoundaryBottom() == self.getExpMaxY())

		# put occupation be at the center of extesion
		problem.appendConstraint(self.getVarExtensionBoundaryCenterX() == self.getVarOccupationBoundaryCenterX())
		problem.appendConstraint(self.getVarExtensionBoundaryCenterY() == self.getVarOccupationBoundaryCenterY())

	def appendConstraintsWithBoundary(self, problem, boundary):
		self.appendConstraintsWithExtensionBoundary(problem, boundary)

	def appendConstraintsWithOccupationBoundary(self, problem, boundary):
		left, top, right, bottom = boundary
		problem.appendConstraint(self.getVarOccupationBoundaryLeft() == left)
		problem.appendConstraint(self.getVarOccupationBoundaryTop() == top)
		problem.appendConstraint(self.getVarOccupationBoundaryRight() == right)
		problem.appendConstraint(self.getVarOccupationBoundaryBottom() == bottom)

	def appendConstraintsWithExtensionBoundary(self, problem, boundary):
		left, top, right, bottom = boundary
		problem.appendConstraint(self.getVarExtensionBoundaryLeft() == left)
		problem.appendConstraint(self.getVarExtensionBoundaryTop() == top)
		problem.appendConstraint(self.getVarExtensionBoundaryRight() == right)
		problem.appendConstraint(self.getVarExtensionBoundaryBottom() == bottom)

	def appendConstraintsWithSizeCenter(self, problem, size, center):
		self.appendConstraintsWithOccupationSizeCenter(problem, size, center)

	def appendConstraintsWithOccupationSizeCenter(self, problem, size, center):
		width, height = size
		centerX, centerY = center
		problem.appendConstraint(self.getVarOccupationBoundaryWidth() == width)
		problem.appendConstraint(self.getVarOccupationBoundaryHeight() == height)
		problem.appendConstraint(self.getVarOccupationBoundaryCenterX() == centerX)
		problem.appendConstraint(self.getVarOccupationBoundaryCenterY() == centerY)

	def appendConstraintsWithExtensionSizeCenter(self, problem, size, center):
		width, height = size
		centerX, centerY = center
		problem.appendConstraint(self.getVarExtensionBoundaryWidth() == width)
		problem.appendConstraint(self.getVarExtensionBoundaryHeight() == height)
		problem.appendConstraint(self.getVarExtensionBoundaryCenterX() == centerX)
		problem.appendConstraint(self.getVarExtensionBoundaryCenterY() == centerY)

	def appendObjective(self, problem):
		problem.appendObjective(Objective(self.getVarOccupationBoundaryWidth() - self.getVarExtensionBoundaryWidth()))
		problem.appendObjective(Objective(self.getVarOccupationBoundaryHeight() - self.getVarExtensionBoundaryHeight()))

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
	@inject
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

	def appendVariables(self, problem):
		super().appendVariables(problem)
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

	def appendConstraints(self, problem):
		super().appendConstraints(problem)
		self.appendConstraintsForPoints(problem)

	def appendObjective(self, problem):
		super().appendObjective(problem)

	def resolvePointStart(self):
		return (self.getVarStartX(), self.getVarStartY())

	def resolvePointEnd(self):
		return (self.getVarEndX(), self.getVarEndY())

