import abc
import uuid

from injector import inject

from .constants import GlyphSolver
from .constants import VariableGenerator

class ConstraintShape(object, metaclass=abc.ABCMeta):
	@inject
	def __init__(self, glyphSolver: GlyphSolver):
		super().__init__()

		self.glyphSolver = glyphSolver

	def getGlyphSolver(self):
		return self.glyphSolver

	def draw(self, drawingSystem):
		raise NotImplementedError('users must define draw to use this base class')

	def appendVariables(self, drawingSystem):
		raise NotImplementedError('users must define appendVariables to use this base class')

	def appendConstraints(self, drawingSystem):
		raise NotImplementedError('users must define appendConstraints to use this base class')

	def appendObjective(self, drawingSystem):
		raise NotImplementedError('users must define appendObjetive to use this base class')

class ConstraintBoundaryShape(ConstraintShape):
	@inject
	def __init__(self):
		super().__init__()

		glyphSolver = self.getGlyphSolver()

		self.uuid = uuid.uuid4()

		componentPrefix = self.getComponentPrefix()
		self.occupationBoundaryLeft = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_left")
		self.occupationBoundaryTop = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_top")
		self.occupationBoundaryRight = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_right")
		self.occupationBoundaryBottom = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_bottom")
		self.occupationBoundaryWidth = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_width")
		self.occupationBoundaryHeight = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_height")
		self.occupationBoundaryCenterX = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_centerX")
		self.occupationBoundaryCenterY = glyphSolver.generateVariable(componentPrefix, "occupation_boundary_centerY")

		self.extensionBoundaryLeft = glyphSolver.generateVariable(componentPrefix, "extension_boundary_left")
		self.extensionBoundaryTop = glyphSolver.generateVariable(componentPrefix, "extension_boundary_top")
		self.extensionBoundaryRight = glyphSolver.generateVariable(componentPrefix, "extension_boundary_right")
		self.extensionBoundaryBottom = glyphSolver.generateVariable(componentPrefix, "extension_boundary_bottom")
		self.extensionBoundaryWidth = glyphSolver.generateVariable(componentPrefix, "extension_boundary_width")
		self.extensionBoundaryHeight = glyphSolver.generateVariable(componentPrefix, "extension_boundary_height")
		self.extensionBoundaryCenterX = glyphSolver.generateVariable(componentPrefix, "extension_boundary_centerX")
		self.extensionBoundaryCenterY = glyphSolver.generateVariable(componentPrefix, "extension_boundary_centerY")

		self.expMinX = self.occupationBoundaryLeft
		self.expMinY = self.occupationBoundaryTop
		self.expMaxX = self.occupationBoundaryRight
		self.expMaxY = self.occupationBoundaryBottom

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
		glyphSolver = self.getGlyphSolver()
		return (
			glyphSolver.interpreteVariable(self.getVarOccupationBoundaryLeft()),
			glyphSolver.interpreteVariable(self.getVarOccupationBoundaryTop()),
			glyphSolver.interpreteVariable(self.getVarOccupationBoundaryRight()),
			glyphSolver.interpreteVariable(self.getVarOccupationBoundaryBottom()),
			)

	def getExtensionBoundary(self):
		glyphSolver = self.getGlyphSolver()
		return (
			glyphSolver.interpreteVariable(self.getVarExtensionBoundaryLeft()),
			glyphSolver.interpreteVariable(self.getVarExtensionBoundaryTop()),
			glyphSolver.interpreteVariable(self.getVarExtensionBoundaryRight()),
			glyphSolver.interpreteVariable(self.getVarExtensionBoundaryBottom()),
			)

	def getOccupationBoundaryCenter(self):
		glyphSolver = self.getGlyphSolver()
		return (glyphSolver.interpreteVariable(self.getVarOccupationBoundaryCenterX()),
			glyphSolver.interpreteVariable(self.getVarOccupationBoundaryCenterY()))

	def getExtensionBoundaryCenter(self):
		glyphSolver = self.getGlyphSolver()
		return (glyphSolver.interpreteVariable(self.getVarExtensionBoundaryCenterX()),
			glyphSolver.interpreteVariable(self.getVarExtensionBoundaryCenterY()))

	def getOccupationSize(self):
		glyphSolver = self.getGlyphSolver()
		return (glyphSolver.interpreteVariable(self.getVarOccupationBoundaryWidth()),
			glyphSolver.interpreteVariable(self.getVarOccupationBoundaryHeight()))

	def getExtensionSize(self):
		glyphSolver = self.getGlyphSolver()
		return (glyphSolver.interpreteVariable(self.getVarExtensionBoundaryWidth()),
			glyphSolver.interpreteVariable(self.getVarExtensionBoundaryHeight()))


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


	def appendVariables(self, drawingSystem):
		drawingSystem.addVariable(self.occupationBoundaryLeft)
		drawingSystem.addVariable(self.occupationBoundaryTop)
		drawingSystem.addVariable(self.occupationBoundaryRight)
		drawingSystem.addVariable(self.occupationBoundaryBottom)
		drawingSystem.addVariable(self.occupationBoundaryWidth)
		drawingSystem.addVariable(self.occupationBoundaryHeight)
		drawingSystem.addVariable(self.occupationBoundaryCenterX)
		drawingSystem.addVariable(self.occupationBoundaryCenterY)

		drawingSystem.addVariable(self.extensionBoundaryLeft)
		drawingSystem.addVariable(self.extensionBoundaryTop)
		drawingSystem.addVariable(self.extensionBoundaryRight)
		drawingSystem.addVariable(self.extensionBoundaryBottom)
		drawingSystem.addVariable(self.extensionBoundaryWidth)
		drawingSystem.addVariable(self.extensionBoundaryHeight)
		drawingSystem.addVariable(self.extensionBoundaryCenterX)
		drawingSystem.addVariable(self.extensionBoundaryCenterY)

	def appendConstraints(self, drawingSystem):
		self.appendConstraintsForBoundary(drawingSystem)

	def appendConstraintsForBoundary(self, drawingSystem):
		# occupation constraints
		drawingSystem.constraintsLe(self.getVarOccupationBoundaryLeft(), self.getVarOccupationBoundaryRight())
		drawingSystem.constraintsLe(self.getVarOccupationBoundaryTop(), self.getVarOccupationBoundaryBottom())
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryCenterX()*2, self.getVarOccupationBoundaryLeft() + self.getVarOccupationBoundaryRight())
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryCenterY()*2, self.getVarOccupationBoundaryTop() + self.getVarOccupationBoundaryBottom())
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryWidth(), self.getVarOccupationBoundaryRight() - self.getVarOccupationBoundaryLeft())
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryHeight(), self.getVarOccupationBoundaryBottom() - self.getVarOccupationBoundaryTop())

		# extension constraints
		drawingSystem.constraintsLe(self.getVarExtensionBoundaryLeft(), self.getVarExtensionBoundaryRight())
		drawingSystem.constraintsLe(self.getVarExtensionBoundaryTop(), self.getVarExtensionBoundaryBottom())
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryCenterX()*2, self.getVarExtensionBoundaryLeft() + self.getVarExtensionBoundaryRight())
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryCenterY()*2, self.getVarExtensionBoundaryTop() + self.getVarExtensionBoundaryBottom())
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryWidth(), self.getVarExtensionBoundaryRight() - self.getVarExtensionBoundaryLeft())
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryHeight(), self.getVarExtensionBoundaryBottom() - self.getVarExtensionBoundaryTop())

		drawingSystem.constraintsLe(self.getVarExtensionBoundaryLeft(), self.getVarOccupationBoundaryLeft())
		drawingSystem.constraintsLe(self.getVarExtensionBoundaryTop(), self.getVarOccupationBoundaryTop())
		drawingSystem.constraintsGe(self.getVarExtensionBoundaryRight(), self.getVarOccupationBoundaryRight())
		drawingSystem.constraintsGe(self.getVarExtensionBoundaryBottom(), self.getVarOccupationBoundaryBottom())

		# make occupation to match the shape
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryLeft(), self.getExpMinX())
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryTop(), self.getExpMinY())
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryRight(), self.getExpMaxX())
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryBottom(), self.getExpMaxY())

		# put occupation be at the center of extesion
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryCenterX(), self.getVarOccupationBoundaryCenterX())
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryCenterY(), self.getVarOccupationBoundaryCenterY())

	def appendConstraintsWithBoundary(self, drawingSystem, boundary):
		self.appendConstraintsWithExtensionBoundary(drawingSystem, boundary)

	def appendConstraintsWithOccupationBoundary(self, drawingSystem, boundary):
		left, top, right, bottom = boundary
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryLeft(), left)
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryTop(), top)
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryRight(), right)
		drawingSystem.constraintsEq(self.getVarOccupationBoundaryBottom(), bottom)

	def appendConstraintsWithExtensionBoundary(self, drawingSystem, boundary):
		left, top, right, bottom = boundary
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryLeft(), left)
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryTop(), top)
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryRight(), right)
		drawingSystem.constraintsEq(self.getVarExtensionBoundaryBottom(), bottom)

	def appendConstraintsWithSizeCenter(self, drawingSystem, size, center):
		width, height = size
		centerX, centerY = center
		drawingSystem.constraintsEq(self.getVarBoundaryWidth(), width)
		drawingSystem.constraintsEq(self.getVarBoundaryHeight(), height)
		drawingSystem.constraintsEq(self.getVarBoundaryCenterX(), centerX)
		drawingSystem.constraintsEq(self.getVarBoundaryCenterY(), centerY)

	def appendObjective(self, drawingSystem):
		drawingSystem.appendObjective(self.getVarOccupationBoundaryWidth())
		drawingSystem.appendObjective(self.getVarOccupationBoundaryHeight())
		drawingSystem.appendObjective(self.getVarExtensionBoundaryWidth() * -1)
		drawingSystem.appendObjective(self.getVarExtensionBoundaryHeight() * -1)

	def resolveScalarOccupationLeft(self):
		return self.occupationBoundaryLeft

	def resolveScalarOccupationTop(self):
		return self.occupationBoundaryTop

	def resolveScalarOccupationRight(self):
		return self.occupationBoundaryRight

	def resolveScalarOccupationBottom(self):
		return self.occupationBoundaryBottom

	def resolveScalarOccupationWidth(self):
		return self.occupationBoundaryWidth

	def resolveScalarOccupationHeight(self):
		return self.occupationBoundaryHeight

	def resolveScalarOccupationCenterX(self):
		return self.occupationBoundaryCenterX

	def resolveScalarOccupationCenterY(self):
		return self.occupationBoundaryCenterY

	def resolvePairOccupationSize(self):
		return (self.resolveScalarOccupationWidth(), self.resolveScalarOccupationHeight())

	def resolvePointOccupationTopLeft(self):
		return (self.resolveScalarOccupationLeft(), self.resolveScalarOccupationTop())

	def resolvePointOccupationTopCenter(self):
		return (self.resolveScalarOccupationCenterX(), self.resolveScalarOccupationTop())

	def resolvePointOccupationTopRight(self):
		return (self.resolveScalarOccupationRight(), self.resolveScalarOccupationTop())

	def resolvePointOccupationLeftCenter(self):
		return (self.resolveScalarOccupationLeft(), self.resolveScalarOccupationCenterY())

	def resolvePointOccupationCenter(self):
		return (self.resolveScalarOccupationCenterX(), self.resolveScalarOccupationCenterY())

	def resolvePointOccupationRightCenter(self):
		return (self.resolveScalarOccupationRight(), self.resolveScalarOccupationCenterY())

	def resolvePointOccupationBottomLeft(self):
		return (self.resolveScalarOccupationLeft(), self.resolveScalarOccupationBottom())

	def resolvePointOccupationBottomCenter(self):
		return (self.resolveScalarOccupationCenterX(), self.resolveScalarOccupationBottom())

	def resolvePointOccupationBottomRight(self):
		return (self.resolveScalarOccupationRight(), self.resolveScalarOccupationBottom())

	def resolveQuaternaryOccupationBoundary(self):
		return (
			self.resolveScalarOccupationLeft(),
			self.resolveScalarOccupationTop(),
			self.resolveScalarOccupationRight(),
			self.resolveScalarOccupationBottom()
			)


	def resolveScalarExtensionLeft(self):
		return self.extensionBoundaryLeft

	def resolveScalarExtensionTop(self):
		return self.extensionBoundaryTop

	def resolveScalarExtensionRight(self):
		return self.extensionBoundaryRight

	def resolveScalarExtensionBottom(self):
		return self.extensionBoundaryBottom

	def resolveScalarExtensionWidth(self):
		return self.extensionBoundaryWidth

	def resolveScalarExtensionHeight(self):
		return self.extensionBoundaryHeight

	def resolveScalarExtensionCenterX(self):
		return self.extensionBoundaryCenterX

	def resolveScalarExtensionCenterY(self):
		return self.extensionBoundaryCenterY

	def resolvePairExtensionSize(self):
		return (self.resolveScalarExtensionWidth(), self.resolveScalarExtensionHeight())

	def resolvePointExtensionTopLeft(self):
		return (self.resolveScalarExtensionLeft(), self.resolveScalarExtensionTop())

	def resolvePointExtensionTopCenter(self):
		return (self.resolveScalarExtensionCenterX(), self.resolveScalarExtensionTop())

	def resolvePointExtensionTopRight(self):
		return (self.resolveScalarExtensionRight(), self.resolveScalarExtensionTop())

	def resolvePointExtensionLeftCenter(self):
		return (self.resolveScalarExtensionLeft(), self.resolveScalarExtensionCenterY())

	def resolvePointExtensionCenter(self):
		return (self.resolveScalarExtensionCenterX(), self.resolveScalarExtensionCenterY())

	def resolvePointExtensionRightCenter(self):
		return (self.resolveScalarExtensionRight(), self.resolveScalarExtensionCenterY())

	def resolvePointExtensionBottomLeft(self):
		return (self.resolveScalarExtensionLeft(), self.resolveScalarExtensionBottom())

	def resolvePointExtensionBottomCenter(self):
		return (self.resolveScalarExtensionCenterX(), self.resolveScalarExtensionBottom())

	def resolvePointExtensionBottomRight(self):
		return (self.resolveScalarExtensionRight(), self.resolveScalarExtensionBottom())

	def resolveQuaternaryExtensionBoundary(self):
		return (
			self.resolveScalarExtensionLeft(),
			self.resolveScalarExtensionTop(),
			self.resolveScalarExtensionRight(),
			self.resolveScalarExtensionBottom()
			)


	def resolveScalarWidth(self):
		return self.resolveScalarExtensionWidth()

	def resolveScalarHeight(self):
		return self.resolveScalarExtensionHeight()

	def resolvePairSize(self):
		return self.resolvePairExtensionSize()

	def resolveQuaternaryBoundary(self):
		return self.resolveExtensionBoundary()

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
		glyphSolver = self.getGlyphSolver()
		self.startX = glyphSolver.generateVariable(componentPrefix, "start_x")
		self.startY = glyphSolver.generateVariable(componentPrefix, "start_y")
		self.endX = glyphSolver.generateVariable(componentPrefix, "end_x")
		self.endY = glyphSolver.generateVariable(componentPrefix, "end_y")

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
		glyphSolver = self.getGlyphSolver()
		return (glyphSolver.interpreteVariable(self.startX),
			glyphSolver.interpreteVariable(self.startY))

	def getEndPoint(self):
		glyphSolver = self.getGlyphSolver()
		return (glyphSolver.interpreteVariable(self.endX),
			glyphSolver.interpreteVariable(self.endY))

	def getVarStartX(self):
		return self.startX

	def getVarStartY(self):
		return self.startY

	def getVarEndX(self):
		return self.endX

	def getVarEndY(self):
		return self.endY

	def appendVariables(self, drawingSystem):
		super().appendVariables(drawingSystem)
		drawingSystem.addVariable(self.startX)
		drawingSystem.addVariable(self.startY)
		drawingSystem.addVariable(self.endX)
		drawingSystem.addVariable(self.endY)

	def appendConstraintsForPoints(self, drawingSystem):
		drawingSystem.constraintsLe(self.getVarBoundaryLeft(), self.startX)
		drawingSystem.constraintsLe(self.getVarBoundaryLeft(), self.endX)

		drawingSystem.constraintsLe(self.getVarBoundaryTop(), self.startY)
		drawingSystem.constraintsLe(self.getVarBoundaryTop(), self.endY)

		drawingSystem.constraintsGe(self.getVarBoundaryRight(), self.startX)
		drawingSystem.constraintsGe(self.getVarBoundaryRight(), self.endX)

		drawingSystem.constraintsGe(self.getVarBoundaryBottom(), self.startY)
		drawingSystem.constraintsGe(self.getVarBoundaryBottom(), self.endY)

	def appendConstraints(self, drawingSystem):
		super().appendConstraints(drawingSystem)
		self.appendConstraintsForPoints(drawingSystem)

	def appendObjective(self, drawingSystem):
		super().appendObjective(drawingSystem)

	def resolvePointStart(self):
		return (self.getVarStartX(), self.getVarStartY())

	def resolvePointEnd(self):
		return (self.getVarEndX(), self.getVarEndY())

