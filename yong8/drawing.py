from injector import inject

from .constants import GlyphSolver

class DrawingGlyphPolicy:
	def __init__(self):
		pass

	def getGlyphSize(self):
		return (255, 255)

	def getMarginHorizontal(self):
		return 40

	def getMarginVertical(self):
		return 20

class DrawingPolicy:
	def __init__(self):
		self.drawingGlyphPolicy = DrawingGlyphPolicy()

	def getDrawingGlyphPolicy(self):
		return self.drawingGlyphPolicy

class ConstraintDrawingSystem:
	@inject
	def __init__(self, glyphSolver: GlyphSolver):
		self.glyphSolver = glyphSolver

		self.drawingPolicy = DrawingPolicy()

	def getDrawingPolicy(self):
		return self.drawingPolicy

	def getDrawingGlyphPolicy(self):
		return self.drawingPolicy.getDrawingGlyphPolicy()

	def getGlyphSolver(self):
		return self.glyphSolver

	def getVariableGenerator(self):
		return self.glyphSolver.getVariableGenerator()

	def addVariable(self, variable):
		from .symbol import Symbol
		if isinstance(variable, Symbol):
			self.glyphSolver.addVariable(variable)
		else:
			raise TypeError("Should be Symbol but is {0}".format(type(variable)))

	def constraints(self, constraint):
		self._appendConstraint(constraint)

	def constraintsEq(self, first, second):
		from .symbol import Eq
		self._appendConstraint(Eq(first, second, evaluate=False))

	def constraintsLe(self, first, second):
		self._appendConstraint(first <= second)

	def constraintsLt(self, first, second):
		self._appendConstraint(first < second)

	def constraintsGe(self, first, second):
		self._appendConstraint(first >= second)

	def constraintsGt(self, first, second):
		self._appendConstraint(first > second)

	def _appendConstraint(self, constraint):
		from .symbol import Relational
		if isinstance(constraint, Relational):
			self.glyphSolver.appendConstraint(constraint)
		else:
			raise TypeError("Should be Relational but is {0}".format(type(constraint)))

	def appendObjective(self, objective):
		from .symbol import Symbol, Expr
		if isinstance(objective, Symbol) or isinstance(objective, Expr):
			self.glyphSolver.appendObjective(objective)
		else:
			raise TypeError("Should be Symbol or Expr but is {0}".format(type(objective)))

	def solve(self):
		self.glyphSolver.solve()

