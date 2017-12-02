import abc

class AbsVariableGenerator(object, metaclass=abc.ABCMeta):
	def generateVariable(self, prefix, name):
		raise NotImplementedError('users must define generateVariable() to use this base class')

	def interpreteVariable(self, variable):
		raise NotImplementedError('users must define interpreteVariable() to use this base class')

class AbsGlyphSolver(object, metaclass=abc.ABCMeta):
	def __init__(self):
		pass

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
		super().__init__()

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

class PuLPGlyphSolver(AbsGlyphSolver):
	def __init__(self, solver):
		super().__init__()

		from pulp import LpProblem
		from pulp import LpMaximize, LpMinimize

		self.prob = LpProblem("myProb", LpMaximize)
		self.solver =solver(msg=False)

	@classmethod
	def generateInstanceByGLPK(cls):
		from pulp import GLPK
		return PuLPGlyphSolver(GLPK)

	@classmethod
	def generateInstanceByCOIN(cls):
		from pulp import COIN
		return PuLPGlyphSolver(COIN)

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

	def solve(self):
		status = self.prob.solve(self.solver)

class CvxpyVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, prefix, name):
		from cvxpy import Variable
		return Variable()

	def interpreteVariable(self, variable):
		return variable.value.item()

class CvxpyGlyphSolver(AbsGlyphSolver):
	def __init__(self, solver):
		super().__init__()

		self.objective = 0
		self.constraints = []
		self.solver = solver

	@classmethod
	def generateInstanceByCBC(cls):
		from cvxpy import CBC
		return CvxpyGlyphSolver(CBC)

	@classmethod
	def generateInstanceByGLPK(cls):
		from cvxpy import GLPK
		return CvxpyGlyphSolver(GLPK)

	@classmethod
	def generateInstanceByCVXOPT(cls):
		from cvxpy import CVXOPT
		return CvxpyGlyphSolver(CVXOPT)

	@classmethod
	def generateInstanceBySCS(cls):
		from cvxpy import SCS
		return CvxpyGlyphSolver(SCS)

	@classmethod
	def generateInstanceByECOS(cls):
		from cvxpy import ECOS
		return CvxpyGlyphSolver(ECOS)

	@classmethod
	def generateInstanceByElemental(cls):
		from cvxpy import ELEMENTAL
		return CvxpyGlyphSolver(ELEMENTAL)

	def getVariableGenerator(self):
		return CvxpyVariableGenerator()

	def addVariable(self, variable):
		pass

	def appendConstraint(self, constraint):
		self.constraints.append(constraint)

	def appendObjective(self, objective):
		self.objective += objective

	def solve(self):
		from cvxpy import Problem
		from cvxpy import Maximize, Minimize
		prob = Problem(Maximize(self.objective), self.constraints)
		prob.solve(self.solver)

