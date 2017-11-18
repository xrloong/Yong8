import abc

class AbsVariableGenerator(object, metaclass=abc.ABCMeta):
	def generateVariable(self, prefix, name):
		raise NotImplementedError('users must define generateVariable() to use this base class')

	def interpreteVariable(self, variable):
		raise NotImplementedError('users must define interpreteVariable() to use this base class')

class AbsGlyphSolver(object, metaclass=abc.ABCMeta):
	def getVariableGenerator(self):
		raise NotImplementedError('users must define getVariableGenerator() to use this base class')

	def addVariable(self, variable):
		raise NotImplementedError('users must define addVariable() to use this base class')

	def appendConstraint(self, constraint):
		raise NotImplementedError('users must define appendConstraint() to use this base class')

	def appendObjective(self, objective):
		raise NotImplementedError('users must define appendObjective() to use this base class')

	def solve(self):
		raise NotImplementedError('users must define solve() to use this base class')

class CassowaryVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, prefix, name):
		from cassowary import Variable
		return Variable(prefix+"."+name)

	def interpreteVariable(self, variable):
		return variable.value

class CassowaryGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		from cassowary import SimplexSolver
		self.solver = SimplexSolver()

	def getVariableGenerator(self):
		return CassowaryVariableGenerator()

	def addVariable(self, variable):
		self.solver.add_var(variable)

	def appendConstraint(self, constraint):
		self.solver.add_constraint(constraint)

	def appendObjective(self, objective):
		from cassowary import STRONG
		self.solver.add_constraint(objective >= 2**32, STRONG)

	def solve(self):
		# Cassowary use incremental solving.
		# It solves the problem during changing constraints.
		pass

class PuLPVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, prefix, name):
		from pulp import LpVariable
		return LpVariable(prefix+"."+name)

	def interpreteVariable(self, variable):
		return variable.value()

class PuLPGlyphSolver(AbsGlyphSolver, metaclass=abc.ABCMeta):
	def __init__(self):
		from pulp import LpProblem
		from pulp import LpMaximize, LpMinimize

		self.prob = LpProblem("myProb", LpMaximize)

	def getVariableGenerator(self):
		return PuLPVariableGenerator()

	def addVariable(self, variable):
		self.prob.addVariable(variable)

	def appendConstraint(self, constraint):
		self.prob += constraint

	def appendObjective(self, objective):
		if self.prob.objective != None:
			self.prob.objective = self.prob.objective + objective
		else:
			self.prob.objective = objective

class GLPKGlyphSolver(PuLPGlyphSolver, metaclass=abc.ABCMeta):
	def solve(self):
		from pulp import GLPK
		status = self.prob.solve(GLPK(msg = False))

class COINGlyphSolver(PuLPGlyphSolver, metaclass=abc.ABCMeta):
	def solve(self):
		from pulp import COIN
		status = self.prob.solve(COIN(msg = False))

