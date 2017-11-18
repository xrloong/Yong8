from .base import BaseTestCase

from yong8.segment import BaseConstraintBeelineSegment
from yong8.segment import BeelineSegment_NN, BeelineSegment_N0, BeelineSegment_NP
from yong8.segment import BeelineSegment_0N, BeelineSegment_00, BeelineSegment_0P
from yong8.segment import BeelineSegment_PN, BeelineSegment_P0, BeelineSegment_PP
from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.constants import GlyphSolver
from yong8.constants import DrawingSystem

class ConstraintSegmentTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testBeelineSegment_NN(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BeelineSegment_NN)

		s.appendVariables(drawingSystem)
		s.appendConstraints(drawingSystem)
		s.appendObjective(drawingSystem)
		s.appendConstraintsWithBoundary(drawingSystem, [38, 61, 182, 129])

		drawingSystem.solve()

		self.assertEqual(s.getBoundary(), (38, 61, 182, 129))
		self.assertEqual(s.getSize(), (144, 68))
		self.assertEqual(s.getStartPoint(), (182.0, 129.0))
		self.assertEqual(s.getEndPoint(), (38.0, 61.0))
		self.assertEqual(s.getBoundaryCenter(), (110.0, 95.0))

	def testBeelineSegment_NP(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BeelineSegment_NP)

		s.appendVariables(drawingSystem)
		s.appendConstraints(drawingSystem)
		s.appendObjective(drawingSystem)
		s.appendConstraintsWithBoundary(drawingSystem, [38, 61, 182, 129])

		drawingSystem.solve()

		self.assertEqual(s.getBoundary(), (38, 61, 182, 129))
		self.assertEqual(s.getSize(), (144, 68))
		self.assertEqual(s.getStartPoint(), (182.0, 61.0))
		self.assertEqual(s.getEndPoint(), (38.0, 129.0))
		self.assertEqual(s.getBoundaryCenter(), (110.0, 95.0))

	def testBeelineSegment_PN(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BeelineSegment_PN)

		s.appendVariables(drawingSystem)
		s.appendConstraints(drawingSystem)
		s.appendObjective(drawingSystem)
		s.appendConstraintsWithBoundary(drawingSystem, [38, 61, 182, 129])

		drawingSystem.solve()

		self.assertEqual(s.getBoundary(), (38, 61, 182, 129))
		self.assertEqual(s.getSize(), (144, 68))
		self.assertEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertEqual(s.getEndPoint(), (182.0, 61.0))
		self.assertEqual(s.getBoundaryCenter(), (110.0, 95.0))

	def testBeelineSegment_PP(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BeelineSegment_PP)

		s.appendVariables(drawingSystem)
		s.appendConstraints(drawingSystem)
		s.appendObjective(drawingSystem)
		s.appendConstraintsWithBoundary(drawingSystem, [38, 61, 182, 129])

		drawingSystem.solve()

		self.assertEqual(s.getBoundary(), (38, 61, 182, 129))
		self.assertEqual(s.getSize(), (144, 68))
		self.assertEqual(s.getStartPoint(), (38.0, 61.0))
		self.assertEqual(s.getEndPoint(), (182.0, 129.0))
		self.assertEqual(s.getBoundaryCenter(), (110.0, 95.0))


	def testSegment_1(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BaseConstraintBeelineSegment)
		s.setDirConfig([1, -1])

		s.appendVariables(drawingSystem)
		s.appendObjective(drawingSystem)
		s.appendConstraintsWithBoundary(drawingSystem, (38, 61, 182, 129))
		s.appendConstraints(drawingSystem)

		drawingSystem.solve()

		self.assertEqual(s.getBoundary(), (38, 61, 182, 129))
		self.assertEqual(s.getSize(), (144, 68))
		self.assertEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertEqual(s.getEndPoint(), (182.0, 61.0))
		self.assertEqual(s.getBoundaryCenter(), (110.0, 95.0))

	def testSegment_2(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BaseConstraintBeelineSegment)
		s.setDirConfig([1, -1])

		s.appendVariables(drawingSystem)
		s.appendConstraints(drawingSystem)
		s.appendObjective(drawingSystem)
		s.appendConstraintsWithSizeCenter(drawingSystem, (144, 68), (110, 95))

		drawingSystem.solve()

		self.assertEqual(s.getBoundary(), (38, 61, 182, 129))
		self.assertEqual(s.getSize(), (144, 68))
		self.assertEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertEqual(s.getEndPoint(), (182.0, 61.0))
		self.assertEqual(s.getBoundaryCenter(), (110.0, 95.0))

