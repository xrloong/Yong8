from enum import Enum

from .constants import Optimization
from .problem import generateVariable
from .problem import Objective
from .shape import ConstraintBoundaryShape

class ConstraintComponent(ConstraintBoundaryShape):
	def __init__(self, strokes):
		super().__init__()

		self.strokes = strokes
		self.compoundConstraints = []

	def dump(self):
		for stroke in self.strokes:
			print("stroke:", stroke)
			print("start point:", stroke.getStartPoint())
			print("end point:", stroke.getEndPoint())
			print()

	def getComponentName(self):
		return "stroke_group"

	def resolve(self, uuid):
		for stroke in self.strokes:
			s = stroke.resolve(uuid)
			if s != None:
				return s
		return None

	def getStrokes(self):
		return self.strokes

	def appendCompoundConstraint(self, compoundConstraint):
		self.compoundConstraints.append(compoundConstraint)

	def appendChildrenProblemTo(self, problem):
		super().appendChildrenProblemTo(problem)

		for stroke in self.getStrokes():
			subProblem = stroke.generateProblem()
			problem.appendProblem(subProblem)

			problem.appendConstraint(self.getVarBoundaryLeft() <= stroke.getVarBoundaryLeft())
			problem.appendConstraint(self.getVarBoundaryTop() <= stroke.getVarBoundaryTop())
			problem.appendConstraint(self.getVarBoundaryRight() >= stroke.getVarBoundaryRight())
			problem.appendConstraint(self.getVarBoundaryBottom() >= stroke.getVarBoundaryBottom())

		for compoundConstraint in self.compoundConstraints:
			problem.appendCompoundConstraint(compoundConstraint)

