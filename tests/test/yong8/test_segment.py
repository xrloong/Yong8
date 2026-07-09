from .base import BaseTestCase
from .base import GlyphSolver

from yong8.factory import SegmentFactory

from yong8.constraint import BoundaryConstraint

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

	def testBeelineSegment_P0(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_P0()

		s.addCompoundConstraint(BoundaryConstraint(s, (38, 61, 182, 61)))

		problem = s.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s.getOccupationBoundary(), (38.0, 61.0, 182.0, 61.0))

	def testBeelineSegment_N0(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_N0()

		s.addCompoundConstraint(BoundaryConstraint(s, (38, 61, 182, 61)))

		problem = s.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s.getOccupationBoundary(), (38.0, 61.0, 182.0, 61.0))

	def testBeelineSegment_0P(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_0P()

		s.addCompoundConstraint(BoundaryConstraint(s, (38, 61, 38, 129)))

		problem = s.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getOccupationBoundary(), (38.0, 61.0, 38.0, 129.0))

	def testBeelineSegment_NN(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_NN()

		s.addCompoundConstraint(BoundaryConstraint(s, (38, 61, 182, 129)))

		problem = s.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s.getOccupationBoundary(), (38.0, 61.0, 182.0, 129.0))

	def testBeelineSegment_NP(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_NP()

		s.addCompoundConstraint(BoundaryConstraint(s, (38, 61, 182, 129)))

		problem = s.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getOccupationBoundary(), (38.0, 61.0, 182.0, 129.0))

	def testBeelineSegment_PN(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_PN()

		s.addCompoundConstraint(BoundaryConstraint(s, (38, 61, 182, 129)))

		problem = s.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s.getOccupationBoundary(), (38.0, 61.0, 182.0, 129.0))

	def testBeelineSegment_PP(self):
		injector = self.getInjector()

		segmentFactory = injector.get(SegmentFactory)
		s = segmentFactory.generateBeelineSegment_PP()

		s.addCompoundConstraint(BoundaryConstraint(s, (38, 61, 182, 129)))

		problem = s.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(s.getOccupationBoundary(), (38.0, 61.0, 182.0, 129.0))


