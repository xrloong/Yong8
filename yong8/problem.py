from .constants import Optimization
from .constraint import CompoundConstraint
from .symbol import V
from .symbol import C
from .symbol import E

def generateVariable(prefix, name, lb=None, ub=None) -> V:
	variableName = prefix+"."+name
	return V(variableName, lb, ub)

class Objective:
	def __init__(self, function, optimization: Optimization):
		self.optimization = optimization
		self.function = function

	def getOptimization(self):
		return self.optimization

	def getFunction(self):
		return self.function

class Problem(CompoundConstraint):
	def __init__(self):
		self.variables = []
		self.constraints = []
		self.objectives = []

	def addVariable(self, variable: V):
		self.variables.append(variable)

	def appendConstraint(self, constraint: C):
		self.constraints.append(constraint)

	def appendObjective(self, function: E, optimization: Optimization = Optimization.Maximize):
		self.objectives.append(Objective(function, optimization))

	def _addAllVariables(self, variables):
		self.variables.extend(variables)

	def _appendAllConstraints(self, constraints):
		self.constraints.extend(constraints)

	def _appendAllObjectives(self, objectives: [Objective]):
		self.objectives.extend(objectives)

	def appendCompoundConstraint(self, constraint: CompoundConstraint):
		self._addAllVariables(constraint.getVariables())
		self._appendAllConstraints(constraint.getConstraints())
		self._appendAllObjectives(constraint.getObjectives())

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

