from .problem import generateVariable
from .shape import ConstraintPath

class ConstraintStroke(ConstraintPath):
	def __init__(self):
		super().__init__()
		componentPrefix = self.getComponentPrefix()
		self.unitWidth = generateVariable(componentPrefix, "unit_width")
		self.unitHeight = generateVariable(componentPrefix, "unit_height")

	def getComponentName(self):
		return "stroke"

	def resolve(self, uuid):
		for segment in self.segments:
			s = segment.resolve(uuid)
			if s != None:
				return s
		return None

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

	def appendVariables(self, problem):
		super().appendVariables(problem)
		problem.addVariable(self.unitWidth)
		problem.addVariable(self.unitHeight)

	def appendConstraints(self, problem):
		super().appendConstraints(problem)

		# Work arround for CVXPY
		problem.appendConstraint(self.unitWidth == self.unitWidth)
		problem.appendConstraint(self.unitHeight == self.unitHeight)

	def appendChildrenProblemTo(self, problem):
		super().appendChildrenProblemTo(problem)

		drawingGlyphPolicy = problem.getDrawingGlyphPolicy()

		for segment in self.getSegments():
			subProblem = segment.generateProblem(drawingGlyphPolicy)
			problem.appendProblem(subProblem)

		# append constraints for arranging segments' width and height
		for segment, weight in zip(self.segments, self.weights):
			w, h = weight
			problem.appendConstraint(self.unitWidth * w == segment.getVarVectorX())
			problem.appendConstraint(self.unitHeight * h == segment.getVarVectorY())

		if self.segments:
			firstSegment = self.segments[0]
			lastSegment = self.segments[-1]

			problem.appendConstraint(self.getVarStartX() == firstSegment.getVarStartX())
			problem.appendConstraint(self.getVarStartY() == firstSegment.getVarStartY())

			for currSegment, nextSegment in zip(self.segments[:-1], self.segments[1:]):
				problem.appendConstraint(currSegment.getVarEndX() == nextSegment.getVarStartX())
				problem.appendConstraint(currSegment.getVarEndY() == nextSegment.getVarStartY())

			problem.appendConstraint(self.getVarEndX() == lastSegment.getVarEndX())
			problem.appendConstraint(self.getVarEndY() == lastSegment.getVarEndY())
		else:
			problem.appendConstraint(self.getVarStartX() == self.getVarEndX())
			problem.appendConstraint(self.getVarStartY() == self.getVarEndY())

