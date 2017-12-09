from injector import inject

from .shape import ConstraintPath

class ConstraintStroke(ConstraintPath):
	@inject
	def __init__(self):
		super().__init__()
		glyphSolver = self.getGlyphSolver()
		componentPrefix = self.getComponentPrefix()
		self.unitWidth = glyphSolver.generateVariable(componentPrefix, "unit_width")
		self.unitHeight = glyphSolver.generateVariable(componentPrefix, "unit_height")

	def getComponentName(self):
		return "stroke"

	def setSegments(self, segments, weights = None):
		if weights == None:
			weights = list(segment.getPathParams().getWeights() for segment in segments)

		self.segments=segments
		self.weights=weights

		accumulatedEndX = 0
		accumulatedEndY = 0
		accumulatedExpressionX = self.getVarStartX()
		accumulatedExpressionY = self.getVarStartY()
		minX = 0
		minY = 0
		maxX = 0
		maxY = 0
		expMinX = accumulatedExpressionX
		expMinY = accumulatedExpressionY
		expMaxX = accumulatedExpressionX
		expMaxY = accumulatedExpressionY
		for segment, weight in zip(segments, weights):
			pathParams = segment.getPathParams()

			rangeWeightStartX = pathParams.getRangeWeightStartX()
			rangeWeightStartY = pathParams.getRangeWeightStartY()
			rangeWeightEndX = pathParams.getRangeWeightEndX()
			rangeWeightEndY = pathParams.getRangeWeightEndY()
			rangeWeightMaxX = pathParams.getRangeWeightMaxX()
			rangeWeightMaxY = pathParams.getRangeWeightMaxY()

			diffWeightMinX = 0 - rangeWeightStartX
			diffWeightMinY = 0 - rangeWeightStartY
			diffWeightMaxX = rangeWeightMaxX - rangeWeightStartX
			diffWeightMaxY = rangeWeightMaxY - rangeWeightStartY
			diffWeightEndX = rangeWeightEndX - rangeWeightStartX
			diffWeightEndY = rangeWeightEndY - rangeWeightStartY

			wW, wH = weight

			if rangeWeightMaxX>0:
				currentMinX = accumulatedEndX + wW * diffWeightMinX/rangeWeightMaxX
				currentMaxX = accumulatedEndX + wW * diffWeightMaxX/rangeWeightMaxX
				accumulatedEndX = accumulatedEndX + wW * diffWeightEndX/rangeWeightMaxX
			else:
				currentMinX = accumulatedEndX
				currentMaxX = accumulatedEndX
				accumulatedEndX = accumulatedEndX

			if rangeWeightMaxY>0:
				currentMinY = accumulatedEndY + wH * diffWeightMinY/rangeWeightMaxY
				currentMaxY = accumulatedEndY + wH * diffWeightMaxY/rangeWeightMaxY
				accumulatedEndY = accumulatedEndY + wH * diffWeightEndY/rangeWeightMaxY
			else:
				currentMinY = accumulatedEndY
				currentMaxY = accumulatedEndY
				accumulatedEndY = accumulatedEndY

			accumulatedExpressionX += segment.getVarVectorX() * diffWeightEndX
			accumulatedExpressionY += segment.getVarVectorY() * diffWeightEndY
			if currentMinX < minX:
				minX = currentMinX
				expMinX = accumulatedExpressionX
			if currentMinY < minY:
				minY = currentMinY
				expMinY = accumulatedExpressionY
			if currentMaxX > maxX:
				maxX = currentMaxX
				expMaxX = accumulatedExpressionX
			if currentMaxY > maxY:
				maxY = currentMaxY
				expMaxY = accumulatedExpressionY
		self.expMinX = expMinX
		self.expMaxX = expMaxX
		self.expMinY = expMinY
		self.expMaxY = expMaxY
		if maxX-minX>0:
			weightSum = maxX-minX
			pathParams.setRangeWeightX((0-minX)/weightSum, (accumulatedEndX-minX)/weightSum)
		else:
			pathParams.setRangeWeightX(0, 0, 0)
		if maxY-minY>0:
			weightSum = maxY-minY
			pathParams.setRangeWeightY((0-minY)/weightSum, (accumulatedEndY-minY)/weightSum)
		else:
			pathParams.setRangeWeightY(0, 0, 0)

	def getSegments(self):
		return self.segments

	def draw(self, drawingSystem):
		pass

	def appendVariables(self, drawingSystem):
		super().appendVariables(drawingSystem)
		drawingSystem.addVariable(self.unitWidth)
		drawingSystem.addVariable(self.unitHeight)
		for segment in self.getSegments():
			segment.appendVariables(drawingSystem)

	def appendConstraints(self, drawingSystem):
		super().appendConstraints(drawingSystem)
		for segment in self.segments:
			segment.appendConstraints(drawingSystem)
			drawingSystem.appendConstraint(self.getVarBoundaryLeft() <= segment.getVarBoundaryLeft())
			drawingSystem.appendConstraint(self.getVarBoundaryTop() <= segment.getVarBoundaryTop())
			drawingSystem.appendConstraint(self.getVarBoundaryRight() >= segment.getVarBoundaryRight())
			drawingSystem.appendConstraint(self.getVarBoundaryBottom() >= segment.getVarBoundaryBottom())

		# append constraints for arranging segments' width and height
		for segment, weight in zip(self.segments, self.weights):
			w, h = weight
			drawingSystem.appendConstraint(self.unitWidth * w == segment.getVarVectorX())
			drawingSystem.appendConstraint(self.unitHeight * h == segment.getVarVectorY())

		if self.segments:
			firstSegment = self.segments[0]
			lastSegment = self.segments[-1]

			drawingSystem.appendConstraint(self.getVarStartX() == firstSegment.getVarStartX())
			drawingSystem.appendConstraint(self.getVarStartY() == firstSegment.getVarStartY())

			for currSegment, nextSegment in zip(self.segments[:-1], self.segments[1:]):
				drawingSystem.appendConstraint(currSegment.getVarEndX() == nextSegment.getVarStartX())
				drawingSystem.appendConstraint(currSegment.getVarEndY() == nextSegment.getVarStartY())

			drawingSystem.appendConstraint(self.getVarEndX() == lastSegment.getVarEndX())
			drawingSystem.appendConstraint(self.getVarEndY() == lastSegment.getVarEndY())
		else:
			drawingSystem.appendConstraint(self.getVarStartX() == self.getVarEndX())
			drawingSystem.appendConstraint(self.getVarStartY() == self.getVarEndY())

	def appendObjective(self, drawingSystem):
		super().appendObjective(drawingSystem)

