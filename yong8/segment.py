from .problem import generateVariable
from .problem import Objective
from .problem import Optimization

from .shape import ConstraintPath

sign = lambda x: x and (1, -1)[x < 0]

class AbsConstraintSegment(ConstraintPath):
	def __init__(self):
		super().__init__()

	def getPointAt(self, t):
		raise NotImplementedError('users must define getPointAt(t) to use this base class')

	def appendConstraintsTo(self, problem):
		super().appendConstraintsTo(problem)

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

class BaseConstraintBeelineSegment(AbsConstraintSegment):
	def __init__(self, dirConfig = None):
		super().__init__()

		componentPrefix = self.getComponentPrefix()
		self.params = [
			generateVariable(componentPrefix, "param_0", lb=0),
			generateVariable(componentPrefix, "param_1", lb=0),
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
			pathParams.setWidthWeight(1)
			pathParams.setRangeWeightX(0, 1)
		elif xDir == -1:
			pathParams.setWidthWeight(1)
			pathParams.setRangeWeightX(1, 0)
		else:
			pathParams.setWidthWeight(0)
			pathParams.setRangeWeightX(0, 0, 0)

		yDir = sign(self.dirConfig[1])
		if yDir == 1:
			pathParams.setHeightWeight(1)
			pathParams.setRangeWeightY(0, 1)
		elif yDir == -1:
			pathParams.setHeightWeight(1)
			pathParams.setRangeWeightY(1, 0)
		else:
			pathParams.setHeightWeight(0)
			pathParams.setRangeWeightY(0, 0, 0)

	def __str__(self):
		return "{1}-{2}, {0}, {3}".format(self.getBoundary(), self.getStartPoint(), self.getEndPoint(), self.params)

	def getPointAt(self, t):
		pointStart = self.getVarStartPoint();
		pointEnd = self.getVarEndPoint();
		return ((1-t) * pointStart[0] + t * pointEnd[0],
			(1-t) * pointStart[1] + t * pointEnd[1])

	def getVarVectorX(self):
		return self.params[0]

	def getVarVectorY(self):
		return self.params[1]

	def getVarVector(self):
		return (self.getVarVectorX(), getVarVectorY())

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

	def appendConstraintsTo(self, problem):
		super().appendConstraintsTo(problem)
		self.appendConstraintsForPath(problem)

	def appendObjectivesTo(self, problem):
		super().appendObjectivesTo(problem)


class BaseConstraintQCurveSegment(AbsConstraintSegment):
	def __init__(self):
		super().__init__()

		componentPrefix = self.getComponentPrefix()
		self.params = [
			generateVariable(componentPrefix, "param_0"),
			generateVariable(componentPrefix, "param_1"),
			generateVariable(componentPrefix, "param_2"),
			generateVariable(componentPrefix, "param_3"),
				]
		self.controllX = generateVariable(componentPrefix, "controll_x")
		self.controllY = generateVariable(componentPrefix, "controll_y")


	def getComponentName(self):
		return "curve_segment"

	def getPointAt(self, t):
		pointStart = self.getVarStartPoint();
		pointControl = self.getVarControlPoint();
		pointEnd = self.getVarEndPoint();
		return ((1-t)*(1-t) * pointStart[0] + 2*(1-t)*t*pointControl[0] + t*t*pointEnd[0],
			(1-t)*(1-t) * pointStart[1] + 2*(1-t)*t*pointControl[1] + t*t*pointEnd[1])

	def getVarVectorX_1(self):
		return self.params[0]

	def getVarVectorY_1(self):
		return self.params[1]

	def getVarVectorX_2(self):
		return self.params[2]

	def getVarVectorY_2(self):
		return self.params[3]

	def getVarVector1(self):
		return (self.getVarVectorX_1(), self.getVarVectorY_1())

	def getVarVector2(self):
		return (self.getVarVectorX_2(), self.getVarVectorY_2())


	def getVarControlX(self):
		return self.controllX

	def getVarControlY(self):
		return self.controllY

	def getVarControlPoint(self):
		return (self.getVarControlX(), self.getVarControlY())

	def getControlPoint(self):
		return (self.getVarControlX().getValue(), self.getVarControlY().getValue())


	def appendVariablesTo(self, problem):
		super().appendVariablesTo(problem)
		for variable in self.params:
			problem.addVariable(variable)
		problem.addVariable(self.getVarControlX())
		problem.addVariable(self.getVarControlY())

	def appendConstraintsTo(self, problem):
		super().appendConstraintsTo(problem)

		problem.appendConstraint(self.getVarControlX() == self.getVarStartX() + self.getVarVectorX_1())
		problem.appendConstraint(self.getVarControlY() == self.getVarStartY() + self.getVarVectorY_1())
		problem.appendConstraint(self.getVarEndX() == self.getVarControlX() + self.getVarVectorX_2())
		problem.appendConstraint(self.getVarEndY() == self.getVarControlY() + self.getVarVectorY_2())

	def appendObjectivesTo(self, problem):
		super().appendObjectivesTo(problem)

