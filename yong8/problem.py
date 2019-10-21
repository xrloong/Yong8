import abc

from .constants import Optimization
from .symbol import V
from .symbol import C

def generateVariable(prefix, name) -> V:
	variableName = prefix+"."+name
	return V(variableName)

class Objective:
	def __init__(self, function, optimization: Optimization = Optimization.Maximize):
		self.optimization = optimization
		self.function = function

	def getOptimization(self):
		return self.optimization

	def getFunction(self):
		return self.function

class AbsProblem(object, metaclass=abc.ABCMeta):
	def getVariables(self):
		raise NotImplementedError('users must define getVariables() to use this base class')

	def getConstraints(self):
		raise NotImplementedError('users must define getConstraints() to use this base class')

	def getObjectives(self):
		raise NotImplementedError('users must define getObjectives() to use this base class')


class Problem:
	def __init__(self):
		self.variables = []
		self.constraints = []
		self.objectives = []

	def addVariable(self, variable: V):
		self.variables.append(variable)

	def appendConstraint(self, constraint: C):
		self.constraints.append(constraint)

	def appendObjective(self, objective: Objective):
		self.objectives.append(objective)

	def _addAllVariables(self, variables):
		for variable in variables:
			self.addVariable(variable)

	def _appendAllConstraints(self, constraints):
		for constraint in constraints:
			self.appendConstraint(constraint)

	def _appendAllObjectives(self, objectives):
		for objective in objectives:
			self.appendObjective(objective)

	def appendProblem(self, problem):
		self._addAllVariables(problem.getVariables())
		self._appendAllConstraints(problem.getConstraints())
		self._appendAllObjectives(problem.getObjectives())

	def getVariables(self):
		return self.variables

	def getConstraints(self):
		return self.constraints

	def getObjectives(self):
		return self.objectives

