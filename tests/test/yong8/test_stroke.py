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

		problem = stroke.generateProblem(drawingSystem)
		stroke.appendConstraintsWithBoundary(problem, (38, 61, 182, 129))

		drawingSystem.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertSequenceAlmostEqual(s.getSize(), (144, 68))
		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s.getBoundaryCenter(), (110.0, 95.0))
		self.assertSequenceAlmostEqual(stroke.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertSequenceAlmostEqual(stroke.getSize(), (144, 68))
		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(stroke.getBoundaryCenter(), (110.0, 95.0))

	def testStroke_2(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s1 = injector.get(BeelineSegment_橫)
		s2 = injector.get(BeelineSegment_豎)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments([s1, s2]);

		problem = stroke.generateProblem(drawingSystem)
		stroke.appendConstraintsWithBoundary(problem, (38, 61, 182, 129))

		drawingSystem.solveProblem(problem)

		self.assertSequenceAlmostEqual(s1.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s1.getEndPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s1.getBoundaryCenter(), (110.0, 61.0))
		self.assertSequenceAlmostEqual(s2.getStartPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s2.getEndPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(s2.getBoundaryCenter(), (182.0, 95.0))
		self.assertSequenceAlmostEqual(stroke.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertSequenceAlmostEqual(stroke.getSize(), (144, 68))
		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(stroke.getBoundaryCenter(), (110.0, 95.0))

	def testStroke_3(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s1 = injector.get(BeelineSegment_橫)
		s2 = injector.get(BeelineSegment_豎)
		s3 = injector.get(BeelineSegment_橫)
		s4 = injector.get(BeelineSegment_豎)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments((s1, s2, s3, s4), ((1, 0), (0, 3), (2, 0), (0, 1)));

		problem = stroke.generateProblem(drawingSystem)
		stroke.appendConstraintsWithBoundary(problem, (38, 61, 182, 129))

		drawingSystem.solveProblem(problem)

		self.assertSequenceAlmostEqual(s1.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s1.getEndPoint(), (86.0, 61.0))
		self.assertSequenceAlmostEqual(s1.getSize(), (48.0, 0.0))
		self.assertSequenceAlmostEqual(s2.getStartPoint(), (86.0, 61.0))
		self.assertSequenceAlmostEqual(s2.getEndPoint(), (86.0, 112.0))
		self.assertSequenceAlmostEqual(s2.getSize(), (0.0, 51.0))
		self.assertSequenceAlmostEqual(s3.getStartPoint(), (86.0, 112.0))
		self.assertSequenceAlmostEqual(s3.getEndPoint(), (182.0, 112.0))
		self.assertSequenceAlmostEqual(s3.getSize(), (96.0, 0.0))
		self.assertSequenceAlmostEqual(s4.getStartPoint(), (182.0, 112.0))
		self.assertSequenceAlmostEqual(s4.getEndPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(s4.getSize(), (0.0, 17.0))
		self.assertSequenceAlmostEqual(stroke.getBoundary(), (38.0, 61.0, 182.0, 129.0))
		self.assertSequenceAlmostEqual(stroke.getSize(), (144, 68))
		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(stroke.getBoundaryCenter(), (110.0, 95.0))

