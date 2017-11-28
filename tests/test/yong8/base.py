import unittest

from yong8.constants import GlyphSolver

class BaseTestCase(unittest.TestCase):
	def setUp(self):
		import warnings
		warnings.filterwarnings("ignore", category=ResourceWarning)
		warnings.filterwarnings("ignore", category=DeprecationWarning)

	def tearDown(self):
		pass

	def getGlyphSolverByCassowary(self):
		from yong8.solver import CassowaryGlyphSolver
		return CassowaryGlyphSolver()

	def getGlyphSolverByPulpGLPK(self):
		from yong8.solver import PuLPGlyphSolver
		return PuLPGlyphSolver.generateInstanceByGLPK()

	def getGlyphSolverByPulpCOIN(self):
		from yong8.solver import PuLPGlyphSolver
		return PuLPGlyphSolver.generateInstanceByCOIN()

	def getGlyphSolver(self):
		return self.getGlyphSolverByPulpCOIN()

	def getInjector(self):
		from injector import Injector
		from yong8.shape import ConstraintShape
		from yong8.drawing_module import DrawingModule

		def configure(binder):
			binder.bind(GlyphSolver, to=self.getGlyphSolver())

		return Injector([configure, DrawingModule()])

	def assertSequenceAlmostEqual(self, seq1, seq2):
		def almost_equal(value_1, value_2):
			return self.assertAlmostEqual(value_1, value_2)

		for values in zip(seq1, seq2):
			almost_equal(*values)

