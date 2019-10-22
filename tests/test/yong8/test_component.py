from .base import BaseTestCase
from .base import GlyphSolver

from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import ConstraintComponent

from yong8.constraint import IntersectionPos
from yong8.constraint import SegmentIntersectionConstraint
from yong8.constraint import PointMatchingConstraint
from yong8.constraint import AlignCenterConstraint
from yong8.constraint import RawConstraint

class ConstraintComponentTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testInjector(self):
		injector = self.getInjector()
		self.assertIsNotNone(injector)

	def testInjectComponentFactory(self):
		injector = self.getInjector()
		componentFactory = injector.get(ComponentFactory)
		self.assertIsNotNone(componentFactory)

	def testComponent_1(self):
		# 一

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke = strokeFactory.橫()
		component = componentFactory.generateComponent([stroke])

		compoundConstraint1 = AlignCenterConstraint(component, stroke)
		compoundConstraint2 = RawConstraint(component.getVarBoundaryWidth() == stroke.getVarBoundaryWidth())

		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint2)


		problem = component.generateProblem()
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (215, 127.5))

	def testComponent_2(self):
		# 十

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		compoundConstraint1 = AlignCenterConstraint(component, stroke1)
		compoundConstraint2 = AlignCenterConstraint(component, stroke2)
		compoundConstraint3 = RawConstraint(component.getVarBoundaryWidth() == stroke1.getVarBoundaryWidth())
		compoundConstraint4 = RawConstraint(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())
		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint2)
		component.appendCompoundConstraint(compoundConstraint3)
		component.appendCompoundConstraint(compoundConstraint4)


		problem = component.generateProblem()
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

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.豎()
		stroke2 = strokeFactory.橫折()
		stroke3 = strokeFactory.橫()

		component = componentFactory.generateComponent([stroke1, stroke2, stroke3])


		compoundConstraint1 = RawConstraint(component.getVarBoundaryWidth() == stroke2.getVarBoundaryWidth())
		compoundConstraint2 = RawConstraint(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())
		compoundConstraint3 = PointMatchingConstraint(stroke1.resolvePointStart(), stroke2.resolvePointStart())
		compoundConstraint4 = PointMatchingConstraint(stroke1.resolvePointEnd(), stroke3.resolvePointStart())
		compoundConstraint5 = PointMatchingConstraint(stroke2.resolvePointEnd(), stroke3.resolvePointEnd())

		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint2)
		component.appendCompoundConstraint(compoundConstraint3)
		component.appendCompoundConstraint(compoundConstraint4)
		component.appendCompoundConstraint(compoundConstraint5)


		problem = component.generateProblem()
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

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0])
		compoundConstraint3 = RawConstraint(component.getVarBoundaryWidth() == stroke1.getVarBoundaryWidth())
		compoundConstraint4 = RawConstraint(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())
		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint3)
		component.appendCompoundConstraint(compoundConstraint4)

		problem = component.generateProblem()

		(t1, t2) = compoundConstraint1.intersections
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

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0], IntersectionPos.BetweenStartEnd, IntersectionPos.Start)
		compoundConstraint3 = RawConstraint(component.getVarBoundaryWidth() == stroke1.getVarBoundaryWidth())
		compoundConstraint4 = RawConstraint(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())

		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint3)
		component.appendCompoundConstraint(compoundConstraint4)

		problem = component.generateProblem()

		(t1, t2) = compoundConstraint1.intersections
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

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.豎()
		stroke2 = strokeFactory.橫折()
		stroke3 = strokeFactory.橫()

		component = componentFactory.generateComponent([stroke1, stroke2, stroke3])

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0], IntersectionPos.Start, IntersectionPos.Start)
		compoundConstraint2 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke3.getSegments()[0], IntersectionPos.End, IntersectionPos.Start)
		compoundConstraint3 = SegmentIntersectionConstraint(stroke2.getSegments()[1], stroke3.getSegments()[0], IntersectionPos.End, IntersectionPos.End)
		compoundConstraint4 = RawConstraint(component.getVarBoundaryWidth() == stroke2.getVarBoundaryWidth())
		compoundConstraint5 = RawConstraint(component.getVarBoundaryHeight() == stroke1.getVarBoundaryHeight())

		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint2)
		component.appendCompoundConstraint(compoundConstraint3)
		component.appendCompoundConstraint(compoundConstraint4)
		component.appendCompoundConstraint(compoundConstraint5)

		problem = component.generateProblem()
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

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()
		stroke3 = strokeFactory.橫()

		component = componentFactory.generateComponent([stroke1, stroke2, stroke3])

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0])
		compoundConstraint2 = SegmentIntersectionConstraint(stroke2.getSegments()[0], stroke3.getSegments()[0], IntersectionPos.End, IntersectionPos.BetweenStartEnd)
		compoundConstraint3 = RawConstraint(component.getVarBoundaryWidth() == stroke3.getVarBoundaryWidth())
		compoundConstraint4 = RawConstraint(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())

		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint2)
		component.appendCompoundConstraint(compoundConstraint3)
		component.appendCompoundConstraint(compoundConstraint4)


		problem = component.generateProblem()
		problem.appendConstraint(stroke1.getVarBoundaryWidth() / stroke3.getVarBoundaryWidth() == 0.9)

		(t1, t2) = compoundConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)
		(t1, t2) = compoundConstraint2.intersections
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

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()
		stroke3 = strokeFactory.橫()

		component = componentFactory.generateComponent([stroke1, stroke2, stroke3])

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0])
		compoundConstraint2 = SegmentIntersectionConstraint(stroke2.getSegments()[0], stroke3.getSegments()[0], IntersectionPos.End, IntersectionPos.BetweenStartEnd)
		compoundConstraint3 = RawConstraint(component.getVarBoundaryWidth() == stroke1.getVarBoundaryWidth())
		compoundConstraint4 = RawConstraint(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())

		component.appendCompoundConstraint(compoundConstraint1)
		component.appendCompoundConstraint(compoundConstraint2)
		component.appendCompoundConstraint(compoundConstraint3)
		component.appendCompoundConstraint(compoundConstraint4)


		problem = component.generateProblem()
		problem.appendConstraint(stroke3.getVarBoundaryWidth() / stroke1.getVarBoundaryWidth() == 0.9)

		(t1, t2) = compoundConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)
		(t1, t2) = compoundConstraint2.intersections
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

