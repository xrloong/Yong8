from .base import BaseTestCase
from .base import GlyphSolver

from yong8.factory import SegmentFactory
from yong8.factory import StrokeFactory

from yong8.constraint import BoundaryConstraint

class ConstraintStrokeTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testInjector(self):
		injector = self.getInjector()
		self.assertIsNotNone(injector)

	def testInjectSegmentFactory(self):
		injector = self.getInjector()
		segmentFactory = injector.get(SegmentFactory)
		self.assertIsNotNone(segmentFactory)

	def testInjectStrokeFactory(self):
		injector = self.getInjector()
		strokeFactory = injector.get(StrokeFactory)
		self.assertIsNotNone(strokeFactory)

	def testStroke_1(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s1 = segmentFactory.generateBeelineSegment_橫()
		s2 = segmentFactory.generateBeelineSegment_豎()

		strokeFactory = injector.get(StrokeFactory)
		stroke = strokeFactory.generateStroke([s1, s2])

		stroke.addCompoundConstraint(BoundaryConstraint(stroke, (38, 61, 182, 129)))

		problem = stroke.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s1.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s1.getEndPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s2.getStartPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s2.getEndPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (182.0, 129.0))

	def testStroke_2(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s1 = segmentFactory.generateBeelineSegment_橫()
		s2 = segmentFactory.generateBeelineSegment_豎()
		s3 = segmentFactory.generateBeelineSegment_橫()
		s4 = segmentFactory.generateBeelineSegment_豎()

		strokeFactory = injector.get(StrokeFactory)
		stroke = strokeFactory.generateStroke((s1, s2, s3, s4), ((1, 0), (0, 3), (2, 0), (0, 1)))

		stroke.addCompoundConstraint(BoundaryConstraint(stroke, (38, 61, 182, 129)))

		problem = stroke.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

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
		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (182.0, 129.0))

