from .base import BaseTestCase

from yong8.segment import BaseConstraintBeelineSegment
from yong8.segment import BeelineSegment_NN, BeelineSegment_N0, BeelineSegment_NP
from yong8.segment import BeelineSegment_0N, BeelineSegment_00, BeelineSegment_0P
from yong8.segment import BeelineSegment_PN, BeelineSegment_P0, BeelineSegment_PP
from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.constants import GlyphSolver
from yong8.drawing import DrawingPolicy

class ConstraintSegmentTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testBeelineSegment_NN(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		s = injector.get(BeelineSegment_NN)

		problem = s.generateProblem(drawingPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (182.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 61.0))

	def testBeelineSegment_NP(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		s = injector.get(BeelineSegment_NP)

		problem = s.generateProblem(drawingPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (182.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (38.0, 129.0))

	def testBeelineSegment_PN(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		s = injector.get(BeelineSegment_PN)

		problem = s.generateProblem(drawingPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))

	def testBeelineSegment_PP(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		s = injector.get(BeelineSegment_PP)

		problem = s.generateProblem(drawingPolicy)
		s.appendConstraintsWithBoundary(problem, [38, 61, 182, 129])

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 61.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 129.0))


	def testSegment_1(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		s = injector.get(BaseConstraintBeelineSegment)
		s.setDirConfig([1, -1])

		problem = s.generateProblem(drawingPolicy)
		s.appendConstraintsWithBoundary(problem, (38, 61, 182, 129))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))

	def testSegment_2(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		s = injector.get(BaseConstraintBeelineSegment)
		s.setDirConfig([1, -1])

		problem = s.generateProblem(drawingPolicy)
		s.appendConstraintsWithSizeCenter(problem, (144, 68), (110, 95))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(s.getStartPoint(), (38.0, 129.0))
		self.assertSequenceAlmostEqual(s.getEndPoint(), (182.0, 61.0))

