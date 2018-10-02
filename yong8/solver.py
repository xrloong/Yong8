import abc

class AbsVariableGenerator(object, metaclass=abc.ABCMeta):
	def generateVariable(self, totalName):
		raise NotImplementedError('users must define generateVariable() to use this base class')

	def interpreteVariable(self, variable):
		raise NotImplementedError('users must define interpreteVariable() to use this base class')

class AbsGlyphSolver(object, metaclass=abc.ABCMeta):
	def __init__(self):
		self.variableGenerator = self.generateVariableGenerator();
		self.variableMap = {}

		self.varibleInToOutMap = {}
		self.varibleOutToInMap = {}

		self.variableCounter = 0

	def getVariableGenerator(self):
		return self.variableGenerator

	def generateVariable(self, prefix, name):
		variableOutName = prefix+"."+name
		variableInName = "x{0}".format(self.variableCounter)
		self.variableCounter += 1

		from .symbol import Symbol
		symbol = Symbol(variableInName)

		solverVariable = self.variableGenerator.generateVariable(variableInName)

		self.variableMap[variableInName] = solverVariable
		self.varibleInToOutMap[variableInName] = variableOutName
		self.varibleOutToInMap[variableOutName] = variableInName

		return symbol

	def getVariableByInName(self, variableInName):
		return self.variableMap[variableInName]

	def interpreteVariable(self, variable):
		return self.variableGenerator.interpreteVariable(self.getSolverVariable(variable))

	def getSolverVariable(self, variable):
		return self.variableMap[variable.name]

	def convertSymExpr(self, symExpr):
		if symExpr.is_Number:
			return float(symExpr)
		elif symExpr.is_Relational:
			from .symbol import Le, Lt, Ge, Gt, Eq
			if isinstance(symExpr, Eq):
				return self.convertSymExpr(symExpr.lhs) == self.convertSymExpr(symExpr.rhs)
			elif isinstance(symExpr, Lt):
				return self.convertSymExpr(symExpr.lhs) < self.convertSymExpr(symExpr.rhs)
			elif isinstance(symExpr, Le):
				return self.convertSymExpr(symExpr.lhs) <= self.convertSymExpr(symExpr.rhs)
			elif isinstance(symExpr, Gt):
				return self.convertSymExpr(symExpr.lhs) > self.convertSymExpr(symExpr.rhs)
			elif isinstance(symExpr, Ge):
				return self.convertSymExpr(symExpr.lhs) >= self.convertSymExpr(symExpr.rhs)
		elif symExpr.is_Symbol:
			variableName=symExpr.name
			return self.getVariableByInName(variableName)

		elif symExpr.is_Add:
			r = 0
			(c, exprs) = symExpr.as_coeff_add()
			r=self.convertSymExpr(c)
			for e in exprs:
				r = r+self.convertSymExpr(e)
			return r
		elif symExpr.is_Mul:
			r = 0
			(c, exprs) = symExpr.as_coeff_mul()
			r=self.convertSymExpr(c)
			for e in exprs:
				r = r*self.convertSymExpr(e)
			return r
		elif symExpr.is_Pow:
			(base, exp)=symExpr.as_base_exp()
			baseVariable = self.convertSymExpr(base)
			expValue = self.convertSymExpr(exp)
			return pow(baseVariable, expValue)
		else:
			return None

	def generateVariableGenerator(self):
		raise NotImplementedError('users must define generateVariableGenerator() to use this base class')
	def addVariable(self, variable):
		raise NotImplementedError('users must define addVariable() to use this base class')

	def appendConstraint(self, constraint):
		raise NotImplementedError('users must define appendConstraint() to use this base class')

	def appendObjective(self, objective):
		raise NotImplementedError('users must define appendObjective() to use this base class')

	def solve(self):
		raise NotImplementedError('users must define solve() to use this base class')

class CassowaryVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, totalName):
		from cassowary import Variable
		return Variable(totalName)

	def interpreteVariable(self, variable):
		return variable.value

class CassowaryGlyphSolver(AbsGlyphSolver):
	def __init__(self):
		super().__init__()

		from cassowary import SimplexSolver
		self.solver = SimplexSolver()

	def generateVariableGenerator(self):
		return CassowaryVariableGenerator()

	def addVariable(self, variable):
		self.solver.add_var(self.getSolverVariable(variable))

	def appendConstraint(self, constraint):
		self.solver.add_constraint(self.convertSymExpr(constraint))

	def appendObjective(self, objective):
		from cassowary import STRONG
		self.solver.add_constraint(self.convertSymExpr(objective) >= 2**32, STRONG)

	def solve(self):
		# Cassowary use incremental solving.
		# It solves the problem during changing constraints.
		pass

class PuLPVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, totalName):
		from pulp import LpVariable
		return LpVariable(totalName)

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

	def generateVariableGenerator(self):
		return PuLPVariableGenerator()

	def addVariable(self, variable):
		self.prob.addVariable(self.getSolverVariable(variable))

	def appendConstraint(self, constraint):
		self.prob += self.convertSymExpr(constraint)

	def appendObjective(self, objective):
		convertedObjective = self.convertSymExpr(objective)
		if self.prob.objective != None:
			self.prob.objective = self.prob.objective + convertedObjective
		else:
			self.prob.objective = convertedObjective

	def solve(self):
		status = self.prob.solve(self.solver)

class CvxpyVariableGenerator(AbsVariableGenerator):
	def generateVariable(self, totalName):
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
	def generateInstanceByECOS(cls):
		from cvxpy import ECOS
		return CvxpyGlyphSolver(ECOS)

	def generateVariableGenerator(self):
		return CvxpyVariableGenerator()

	def addVariable(self, variable):
		pass

	def appendConstraint(self, constraint):
		self.constraints.append(self.convertSymExpr(constraint))

	def appendObjective(self, objective):
		self.objective += self.convertSymExpr(objective)

	def solve(self):
		from cvxpy import Problem
		from cvxpy import Maximize, Minimize
		prob = Problem(Maximize(self.objective), self.constraints)
		prob.solve(self.solver)

