from .problem import generateVariable
from .shape import ConstraintPath

sign = lambda x: x and (1, -1)[x < 0]

class BaseConstraintBeelineSegment(ConstraintPath):
	def __init__(self, dirConfig = None):
		super().__init__()

		componentPrefix = self.getComponentPrefix()
		self.params = [
			generateVariable(componentPrefix, "param_0"),
			generateVariable(componentPrefix, "param_1"),
			]
		self.setDirConfig(dirConfig)

	def getComponentName(self):
		return "beeline_segment"

	def setDirConfig(self, dirConfig):
		self.dirConfig = dirConfig

		if not dirConfig:
			return

		pathParams = self.getPathParams()
		xDir = sign(self.dirConfig[0])
		if xDir == 1:
			self.expMinX = self.getVarStartX()
			self.expMaxX = self.getVarEndX()
			pathParams.setWidthWeight(1)
			pathParams.setRangeWeightX(0, 1)
		elif xDir == -1:
			self.expMinX = self.getVarEndX()
			self.expMaxX = self.getVarStartX()
			pathParams.setWidthWeight(1)
			pathParams.setRangeWeightX(1, 0)
		else:
			self.expMinX = self.getVarStartX()
			self.expMaxX = self.getVarStartX()
			pathParams.setWidthWeight(0)
			pathParams.setRangeWeightX(0, 0, 0)

		yDir = sign(self.dirConfig[1])
		if yDir == 1:
			self.expMinY = self.getVarStartY()
			self.expMaxY = self.getVarEndY()
			pathParams.setHeightWeight(1)
			pathParams.setRangeWeightY(0, 1)
		elif yDir == -1:
			self.expMinY = self.getVarEndY()
			self.expMaxY = self.getVarStartY()
			pathParams.setHeightWeight(1)
			pathParams.setRangeWeightY(1, 0)
		else:
			self.expMinY = self.getVarStartY()
			self.expMaxY = self.getVarStartY()
			pathParams.setHeightWeight(0)
			pathParams.setRangeWeightY(0, 0, 0)

	def __str__(self):
		return "{1}-{2}, {0}, {3}".format(self.getBoundary(), self.getStartPoint(), self.getEndPoint(), self.params)

	def getPointAt(self, t):
		pointStart = self.resolvePointStart();
		pointEnd = self.resolvePointEnd();
		return ((1-t) * pointStart[0] + t * pointEnd[0],
			(1-t) * pointStart[1] + t * pointEnd[1])

	def getVarVectorX(self):
		return self.params[0]

	def getVarVectorY(self):
		return self.params[1]

	def appendVariablesTo(self, problem):
		super().appendVariablesTo(problem)
		for variable in self.params:
			problem.addVariable(variable)

	def appendConstraintsForPath(self, problem):
		constraints = ()
		if self.dirConfig:
			cs = []
			xDir = sign(self.dirConfig[0])
			yDir = sign(self.dirConfig[1])
			if xDir == 1:
				problem.appendConstraint(self.getVarStartX() + self.getVarVectorX() == self.getVarEndX())
				problem.appendConstraint(self.getVarBoundaryLeft() == self.getVarStartX())
				problem.appendConstraint(self.getVarBoundaryRight() == self.getVarEndX())
			elif xDir == -1:
				problem.appendConstraint(self.getVarStartX() - self.getVarVectorX() == self.getVarEndX())
				problem.appendConstraint(self.getVarBoundaryLeft() == self.getVarEndX())
				problem.appendConstraint(self.getVarBoundaryRight() == self.getVarStartX())
			else:
				problem.appendConstraint(self.getVarBoundaryLeft() == self.getVarStartX())
				problem.appendConstraint(self.getVarBoundaryRight() == self.getVarEndX())
				problem.appendConstraint(self.getVarStartX() == self.getVarEndX())
				problem.appendConstraint(self.getVarVectorX() == 0)
				problem.appendConstraint(self.getVarBoundaryWidth() == 0)
			problem.appendConstraint(self.getVarVectorX() >= 0 )

			if yDir == 1:
				problem.appendConstraint(self.getVarBoundaryTop() == self.getVarStartY())
				problem.appendConstraint(self.getVarBoundaryBottom() == self.getVarEndY())
				problem.appendConstraint(self.getVarStartY() + self.getVarVectorY() == self.getVarEndY())
			elif yDir == -1:
				problem.appendConstraint(self.getVarBoundaryTop() == self.getVarEndY())
				problem.appendConstraint(self.getVarBoundaryBottom() == self.getVarStartY())
				problem.appendConstraint(self.getVarStartY() - self.getVarVectorY() == self.getVarEndY())
			else:
				problem.appendConstraint(self.getVarBoundaryTop() == self.getVarStartY())
				problem.appendConstraint(self.getVarBoundaryBottom() == self.getVarEndY())
				problem.appendConstraint(self.getVarStartY() == self.getVarEndY())
				problem.appendConstraint(self.getVarVectorY() == 0)
				problem.appendConstraint(self.getVarBoundaryHeight() == 0)
			problem.appendConstraint(self.getVarVectorY() >= 0 )

	def appendConstraintsForPoints(self, problem):
		super().appendConstraintsForPoints(problem)
		self.appendConstraintsForPath(problem)

	def appendObjectivesTo(self, problem):
		super().appendObjectivesTo(problem)



class BaseConstraintQCurveSegment(ConstraintPath):
	def __init__(self):
		super().__init__()

		componentPrefix = self.getComponentPrefix()
		self.params = [
			generateVariable(componentPrefix, "param_0"),
			generateVariable(componentPrefix, "param_1"),
			generateVariable(componentPrefix, "param_2"),
			generateVariable(componentPrefix, "param_3"),
				]

	def getComponentName(self):
		return "curve_segment"

	def getVarVectorX_1(self):
		return self.params[0]

	def getVarVectorY_1(self):
		return self.params[1]

	def getVarVectorX_2(self):
		return self.params[2]

	def getVarVectorY_2(self):
		return self.params[3]

	def appendVariablesTo(self, problem):
		super().appendVariablesTo(problem)
		for variable in self.params:
			problem.addVariable(variable)

	def appendConstraintsForPath(self):
		return (
			self.getVarStartX() + self.getVarVectorX_1() + self.getVarVectorX_2() == self.getVarEndX(),
			self.getVarStartY() + self.getVarVectorY_1() + self.getVarVectorY_2() == self.getVarEndY(),
			)

