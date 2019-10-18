from .base import BaseTestCase
from .base import GlyphSolver

from yong8.drawing import DrawingGlyphPolicy
from yong8.factory import SegmentFactory

class ConstraintSegmentTestCase(BaseTestCase):
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

	def testBeelineSegment_NN(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_NN()

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = s.generateProblem(drawingGlyphPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 61.0))

	def testBeelineSegment_NP(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_NP()

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = s.generateProblem(drawingGlyphPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 129.0))

	def testBeelineSegment_PN(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_PN()

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = s.generateProblem(drawingGlyphPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))

	def testBeelineSegment_PP(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_PP()

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = s.generateProblem(drawingGlyphPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 129.0))


	def testSegment_1(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment([1, -1])

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = s.generateProblem(drawingGlyphPolicy)
		s.appendConstraintsWithBoundary(problem, (38, 61, 182, 129))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))

	def testSegment_2(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment([1, -1])

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = s.generateProblem(drawingGlyphPolicy)
		s.appendConstraintsWithSizeCenter(problem, (144, 68), (110, 95))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))

