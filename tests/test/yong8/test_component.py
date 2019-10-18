from .base import BaseTestCase
from .base import GlyphSolver

from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.stroke import ConstraintStroke
from yong8.component import LayoutConstraint
from yong8.component import ConstraintComponent
from yong8.component import IntersectionPos
from yong8.drawing import DrawingGlyphPolicy

class ConstraintComponentTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testComponent_1(self):
		# 一

		injector = self.getInjector()

		s = injector.get(BeelineSegment_橫)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments([s]);
		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsAlignCenter(stroke)

		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAsRow(component.getVarOccupationBoundaryWidth() == stroke.getVarOccupationBoundaryWidth())

		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsMinimize(component.getVarOccupationBoundaryHeight()*2)

		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (215, 127.5))

	def testComponent_2(self):
		# 十

		injector = self.getInjector()

		s1 = injector.get(BeelineSegment_橫)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsAlignCenter(stroke1)
		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAsAlignCenter(stroke2)
		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsRow(component.getVarOccupationBoundaryWidth() == stroke1.getVarOccupationBoundaryWidth())
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsRow(component.getVarOccupationBoundaryHeight() == stroke2.getVarOccupationBoundaryHeight())
		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (215, 127.5))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

	def testComponent_3(self):
		# 口

		injector = self.getInjector()

		s1 = injector.get(BeelineSegment_豎)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2_1 = injector.get(BeelineSegment_橫)
		s2_2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2_1, s2_2]);

		s3 = injector.get(BeelineSegment_橫)
		stroke3 = injector.get(ConstraintStroke)
		stroke3.setSegments([s3]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2, stroke3])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsRow(component.getVarOccupationBoundaryWidth() == stroke2.getVarOccupationBoundaryWidth())
		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAsRow(component.getVarOccupationBoundaryHeight() == stroke2.getVarOccupationBoundaryHeight())

		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsPointMatchPoint(stroke1.resolvePointStart(), stroke2.resolvePointStart())
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsPointMatchPoint(stroke1.resolvePointEnd(), stroke3.resolvePointStart())
		layoutConstraint5 = LayoutConstraint()
		layoutConstraint5.setAsPointMatchPoint(stroke2.resolvePointEnd(), stroke3.resolvePointEnd())

		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)
		component.appendLayoutConstraint(layoutConstraint5)


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (40.0, 20.0))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (215.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (215.0, 235.0))

	def testComponent_4(self):
		# 十

		injector = self.getInjector()

		s1 = injector.get(BeelineSegment_橫)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsSegmentsIntersection(s1, s2)
		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsRow(component.getVarOccupationBoundaryWidth() == stroke1.getVarOccupationBoundaryWidth())
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsRow(component.getVarOccupationBoundaryHeight() == stroke2.getVarOccupationBoundaryHeight())
		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)

		(t1, t2) = layoutConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (215, 127.5))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

	def testComponent_5(self):
		# 丅

		injector = self.getInjector()

		s1 = injector.get(BeelineSegment_橫)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsSegmentsIntersection(s1, s2, IntersectionPos.BetweenStartEnd, IntersectionPos.Start)
		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsRow(component.getVarOccupationBoundaryWidth() == stroke1.getVarOccupationBoundaryWidth())
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsRow(component.getVarOccupationBoundaryHeight() == stroke2.getVarOccupationBoundaryHeight())
		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)

		(t1, t2) = layoutConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40, 20.0))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (215, 20.0))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

	def testComponent_6(self):
		# 口

		injector = self.getInjector()

		s1 = injector.get(BeelineSegment_豎)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2_1 = injector.get(BeelineSegment_橫)
		s2_2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2_1, s2_2]);

		s3 = injector.get(BeelineSegment_橫)
		stroke3 = injector.get(ConstraintStroke)
		stroke3.setSegments([s3]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2, stroke3])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsSegmentsIntersection(s1, s2_1, IntersectionPos.Start, IntersectionPos.Start)
		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAsSegmentsIntersection(s1, s3, IntersectionPos.End, IntersectionPos.Start)
		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsSegmentsIntersection(s2_2, s3, IntersectionPos.End, IntersectionPos.End)
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsRow(component.getVarOccupationBoundaryWidth() == stroke2.getVarOccupationBoundaryWidth())
		layoutConstraint5 = LayoutConstraint()
		layoutConstraint5.setAsRow(component.getVarOccupationBoundaryHeight() == stroke1.getVarOccupationBoundaryHeight())


		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)
		component.appendLayoutConstraint(layoutConstraint5)


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40.0, 20.0))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (40.0, 20.0))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (215.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (215.0, 235.0))


	def testComponent_7(self):
		# 土

		injector = self.getInjector()

		s1 = injector.get(BeelineSegment_橫)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2]);

		s3 = injector.get(BeelineSegment_橫)
		stroke3 = injector.get(ConstraintStroke)
		stroke3.setSegments([s3]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2, stroke3])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsSegmentsIntersection(s1, s2)
		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAsSegmentsIntersection(s2, s3, IntersectionPos.End, IntersectionPos.BetweenStartEnd)
		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsRow(component.getVarOccupationBoundaryWidth() == stroke3.getVarOccupationBoundaryWidth())
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsRow(component.getVarOccupationBoundaryHeight() == stroke2.getVarOccupationBoundaryHeight())
		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)



		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)
		problem.appendConstraint(stroke1.getVarOccupationBoundaryWidth() / stroke3.getVarOccupationBoundaryWidth() == 0.9)

		(t1, t2) = layoutConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)
		(t1, t2) = layoutConstraint2.intersections
		problem.appendConstraint(t2==0.5)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (48.75, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (206.25, 127.5))

		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (40, 235))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (215, 235))

	def testComponent_8(self):
		# 士

		injector = self.getInjector()

		s1 = injector.get(BeelineSegment_橫)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2]);

		s3 = injector.get(BeelineSegment_橫)
		stroke3 = injector.get(ConstraintStroke)
		stroke3.setSegments([s3]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2, stroke3])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAsSegmentsIntersection(s1, s2)
		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAsSegmentsIntersection(s2, s3, IntersectionPos.End, IntersectionPos.BetweenStartEnd)
		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsRow(component.getVarOccupationBoundaryWidth() == stroke1.getVarOccupationBoundaryWidth())
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsRow(component.getVarOccupationBoundaryHeight() == stroke2.getVarOccupationBoundaryHeight())
		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = component.generateProblem(drawingGlyphPolicy)
		problem.appendConstraint(stroke3.getVarOccupationBoundaryWidth() / stroke1.getVarOccupationBoundaryWidth() == 0.9)

		(t1, t2) = layoutConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)
		(t1, t2) = layoutConstraint2.intersections
		problem.appendConstraint(t2==0.5)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (215, 127.5))

		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (48.75, 235))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (206.25, 235))

