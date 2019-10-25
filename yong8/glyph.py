from .shape import ConstraintBoundaryShape

class ConstraintGlyph(ConstraintBoundaryShape):
	def __init__(self, components):
		super().__init__()

		self.components = components
		componentPrefix = self.getComponentPrefix()

	def getComponentName(self):
		return "glyph"

	def resolve(self, uuid):
		for component in self.components:
			c = componenet.resolve(uuid)
			if c != None:
				return c
		return None

	def getComponents(self):
		return self.components

	def appendChildrenProblemTo(self, problem):
		super().appendChildrenProblemTo(problem)

		for component in self.getComponents():
			subProblem = component.generateProblem()
			problem.appendProblem(subProblem)

