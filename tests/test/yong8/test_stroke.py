from .base import BaseTestCase

from yong8.segment import BaseConstraintBeelineSegment
from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.stroke import ConstraintStroke
from yong8.constants import GlyphSolver
from yong8.constants import DrawingSystem

class ConstraintStrokeTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testStroke_1(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BaseConstraintBeelineSegment)
		s.setDirConfig([1, -1])
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments([s]);

		stroke.appendVariables(drawingSystem)
		stroke.appendConstraints(drawingSystem)
		stroke.appendConstraintsWithBoundary(drawingSystem, (38, 61, 182, 129))
		stroke.appendObjective(drawingSystem)

		drawingSystem.solve()

		self.assertEqual(s.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertEqual(s.getSize(), (144, 68))
		self.assertEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertEqual(s.getEndPoint(), (182.0, 61.0))
		self.assertEqual(s.getBoundaryCenter(), (110.0, 95.0))
		self.assertEqual(stroke.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertEqual(stroke.getSize(), (144, 68))
		self.assertEqual(stroke.getStartPoint(), (38.0, 129.0))
		self.assertEqual(stroke.getEndPoint(), (182.0, 61.0))
		self.assertEqual(stroke.getBoundaryCenter(), (110.0, 95.0))

	def testStroke_2(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s1 = injector.get(BeelineSegment_橫)
		s2 = injector.get(BeelineSegment_豎)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments([s1, s2]);

		stroke.appendVariables(drawingSystem)
		stroke.appendConstraints(drawingSystem)
		stroke.appendConstraintsWithBoundary(drawingSystem, (38, 61, 182, 129))
		stroke.appendObjective(drawingSystem)

		drawingSystem.solve()

		self.assertEqual(s1.getStartPoint(), (38.0, 61.0))
		self.assertEqual(s1.getEndPoint(), (182.0, 61.0))
		self.assertEqual(s1.getBoundaryCenter(), (110.0, 61.0))
		self.assertEqual(s2.getStartPoint(), (182.0, 61.0))
		self.assertEqual(s2.getEndPoint(), (182.0, 129.0))
		self.assertEqual(s2.getBoundaryCenter(), (182.0, 95.0))
		self.assertEqual(stroke.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertEqual(stroke.getSize(), (144, 68))
		self.assertEqual(stroke.getStartPoint(), (38.0, 61.0))
		self.assertEqual(stroke.getEndPoint(), (182.0, 129.0))
		self.assertEqual(stroke.getBoundaryCenter(), (110.0, 95.0))

	def testStroke_3(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s1 = injector.get(BeelineSegment_橫)
		s2 = injector.get(BeelineSegment_豎)
		s3 = injector.get(BeelineSegment_橫)
		s4 = injector.get(BeelineSegment_豎)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments((s1, s2, s3, s4), ((1, 0), (0, 3), (2, 0), (0, 1)));

		stroke.appendVariables(drawingSystem)
		stroke.appendConstraints(drawingSystem)
		stroke.appendConstraintsWithBoundary(drawingSystem, (38, 61, 182, 129))
		stroke.appendObjective(drawingSystem)

		drawingSystem.solve()

		self.assertEqual(s1.getStartPoint(), (38.0, 61.0))
		self.assertEqual(s1.getEndPoint(), (86.0, 61.0))
		self.assertEqual(s1.getSize(), (48.0, 0.0))
		self.assertEqual(s2.getStartPoint(), (86.0, 61.0))
		self.assertEqual(s2.getEndPoint(), (86.0, 112.0))
		self.assertEqual(s2.getSize(), (0.0, 51.0))
		self.assertEqual(s3.getStartPoint(), (86.0, 112.0))
		self.assertEqual(s3.getEndPoint(), (182.0, 112.0))
		self.assertEqual(s3.getSize(), (96.0, 0.0))
		self.assertEqual(s4.getStartPoint(), (182.0, 112.0))
		self.assertEqual(s4.getEndPoint(), (182.0, 129.0))
		self.assertEqual(s4.getSize(), (0.0, 17.0))
		self.assertEqual(stroke.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertEqual(stroke.getSize(), (144, 68))
		self.assertEqual(stroke.getStartPoint(), (38.0, 61.0))
		self.assertEqual(stroke.getEndPoint(), (182.0, 129.0))
		self.assertEqual(stroke.getBoundaryCenter(), (110.0, 95.0))
