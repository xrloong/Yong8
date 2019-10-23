from .problem import generateVariable
from .problem import Objective
from .problem import Optimization
from .shape import ConstraintPath

class ConstraintStroke(ConstraintPath):
	def __init__(self, segments, weights = None):
		super().__init__()
		componentPrefix = self.getComponentPrefix()
		self.unitWidth = generateVariable(componentPrefix, "unit_width")
		self.unitHeight = generateVariable(componentPrefix, "unit_height")

		self._setSegments(segments, weights)

	def getComponentName(self):
		return "stroke"

	def resolve(self, uuid):
		for segment in self.segments:
			s = segment.resolve(uuid)
			if s != None:
				return s
		return None

	def _setSegments(self, segments, weights = None):
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
			if currentMinY < minY:
				minY = currentMinY
			if currentMaxX > maxX:
				maxX = currentMaxX
			if currentMaxY > maxY:
				maxY = currentMaxY
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

	def appendVariablesTo(self, problem):
		super().appendVariablesTo(problem)
		problem.addVariable(self.unitWidth)
		problem.addVariable(self.unitHeight)

	def appendConstraintsTo(self, problem):
		super().appendConstraintsTo(problem)

		# Work arround for CVXPY
		problem.appendConstraint(self.unitWidth == self.unitWidth)
		problem.appendConstraint(self.unitHeight == self.unitHeight)

		for segment in self.getSegments():
			problem.appendConstraint(self.getVarMinX() <= segment.getVarMinX())
			problem.appendConstraint(self.getVarMinY() <= segment.getVarMinY())
			problem.appendConstraint(self.getVarMaxX() >= segment.getVarMaxX())
			problem.appendConstraint(self.getVarMaxY() >= segment.getVarMaxY())

	def appendChildrenProblemTo(self, problem):
		super().appendChildrenProblemTo(problem)

		for segment in self.getSegments():
			subProblem = segment.generateProblem()
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

	def appendObjectivesTo(self, problem):
		super().appendObjectivesTo(problem)

		for segment in self.getSegments():
			problem.appendObjective(Objective(10*(segment.getVarMinX() - self.getVarMinX()), Optimization.Minimize))
			problem.appendObjective(Objective(10*(segment.getVarMinY() - self.getVarMinY()), Optimization.Minimize))
			problem.appendObjective(Objective(10*(self.getVarMaxX() - segment.getVarMaxX()), Optimization.Minimize))
			problem.appendObjective(Objective(10*(self.getVarMaxY() - segment.getVarMaxY()), Optimization.Minimize))

