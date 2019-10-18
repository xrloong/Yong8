import unittest

from injector import Key

GlyphSolver = Key('GlyphSolver')

class BaseTestCase(unittest.TestCase):
	def setUp(self):
		import warnings
		warnings.filterwarnings("ignore", category=ResourceWarning)
		warnings.filterwarnings("ignore", category=DeprecationWarning)

	def tearDown(self):
		pass

	def getInjector(self):
		from injector import Injector
		from yong8.shape import ConstraintShape
		from .injection import DrawingModule
		from .injection import FactoryModule

		from solver import Solver

		def configure(binder):
			binder.bind(GlyphSolver, to=Solver())

		return Injector([configure, DrawingModule(), FactoryModule()])

	def assertSequenceAlmostEqual(self, seq1, seq2):
		def almost_equal(value_1, value_2):
			return self.assertAlmostEqual(value_1, value_2)

		for values in zip(seq1, seq2):
			almost_equal(*values)

