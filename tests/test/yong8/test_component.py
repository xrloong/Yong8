from .base import BaseTestCase
from .base import GlyphSolver

from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import ConstraintComponent

from yong8.constraint import IntersectionPos
from yong8.constraint import SegmentIntersectionConstraint
from yong8.constraint import BoundaryConstraint
from yong8.constraint import SymmetricConstraint

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

	def testResolve(self):
		import uuid

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		segment1 = stroke1.getSegments()[0]
		segment2 = stroke2.getSegments()[0]
		self.assertIs(component.resolve(segment1.getId()), segment1)
		self.assertIs(component.resolve(segment2.getId()), segment2)
		self.assertIsNone(component.resolve(uuid.uuid4()))

	def testComponent_1(self):
		# 一

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke = strokeFactory.橫()
		component = componentFactory.generateComponent([stroke])

		compoundConstraint1 = SymmetricConstraint(component, stroke)
		component.addCompoundConstraint(compoundConstraint1)

		component.addCompoundConstraint(BoundaryConstraint(component, (40, 20, 215, 235)))

		problem = component.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (215, 127.5))

	def testComponent_2(self):
		# 丨

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke = strokeFactory.豎()
		component = componentFactory.generateComponent([stroke])

		compoundConstraint1 = SymmetricConstraint(component, stroke)
		component.addCompoundConstraint(compoundConstraint1)

		component.addCompoundConstraint(BoundaryConstraint(component, (40, 20, 215, 235)))

		problem = component.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (127.5, 235))

	def testComponent_3(self):
		# 十

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0])
		component.addCompoundConstraint(compoundConstraint1)

		component.addCompoundConstraint(BoundaryConstraint(component, (40, 20, 215, 235)))

		problem = component.generateProblem()

		(t1, t2) = compoundConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (215, 127.5))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

	def testSegmentIntersectionPoint(self):
		# 十, verifying the solved intersection point

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0])
		component.addCompoundConstraint(compoundConstraint1)

		component.addCompoundConstraint(BoundaryConstraint(component, (40, 20, 215, 235)))

		problem = component.generateProblem()

		(t1, t2) = compoundConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertAlmostEqual(compoundConstraint1.intersectionX.getValue(), 127.5)
		self.assertAlmostEqual(compoundConstraint1.intersectionY.getValue(), 127.5)
		self.assertAlmostEqual(t1.getValue(), 0.5)
		self.assertAlmostEqual(t2.getValue(), 0.5)

	def testSegmentIntersection_AfterEnd(self):
		# 橫 ends before reaching 豎; their extensions cross at t1 > 1

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		stroke1.addCompoundConstraint(BoundaryConstraint(stroke1, (40, 127.5, 100, 127.5)))
		stroke2.addCompoundConstraint(BoundaryConstraint(stroke2, (150, 20, 150, 235)))

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0], IntersectionPos.AfterEnd, IntersectionPos.BetweenStartEnd)
		component.addCompoundConstraint(compoundConstraint1)

		problem = component.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		(t1, t2) = compoundConstraint1.intersections
		self.assertAlmostEqual(compoundConstraint1.intersectionX.getValue(), 150.0, places=4)
		self.assertAlmostEqual(compoundConstraint1.intersectionY.getValue(), 127.5, places=4)
		self.assertAlmostEqual(t1.getValue(), 110/60, places=4)
		self.assertAlmostEqual(t2.getValue(), 0.5, places=4)

	def testSegmentIntersection_BeforeStart(self):
		# 豎 stands before 橫 starts; their extensions cross at t1 < 0

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component = componentFactory.generateComponent([stroke1, stroke2])

		stroke1.addCompoundConstraint(BoundaryConstraint(stroke1, (100, 127.5, 215, 127.5)))
		stroke2.addCompoundConstraint(BoundaryConstraint(stroke2, (50, 20, 50, 235)))

		compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0], IntersectionPos.BeforeStart, IntersectionPos.BetweenStartEnd)
		component.addCompoundConstraint(compoundConstraint1)

		problem = component.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		(t1, t2) = compoundConstraint1.intersections
		self.assertAlmostEqual(compoundConstraint1.intersectionX.getValue(), 50.0, places=4)
		self.assertAlmostEqual(compoundConstraint1.intersectionY.getValue(), 127.5, places=4)
		self.assertAlmostEqual(t1.getValue(), -50/115, places=4)
		self.assertAlmostEqual(t2.getValue(), 0.5, places=4)

	def testComponent_4(self):
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

		component.addCompoundConstraint(compoundConstraint1)
		component.addCompoundConstraint(compoundConstraint2)
		component.addCompoundConstraint(compoundConstraint3)

		component.addCompoundConstraint(BoundaryConstraint(component, (40, 20, 215, 235)))

		problem = component.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40.0, 20.0))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (40.0, 20.0))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (215.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (215.0, 235.0))


	def testComponent_5(self):
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

		component.addCompoundConstraint(compoundConstraint1)
		component.addCompoundConstraint(compoundConstraint2)

		component.addCompoundConstraint(BoundaryConstraint(component, (40, 20, 215, 235)))

		problem = component.generateProblem()
		problem.appendConstraint(stroke1.getVarBoundaryWidth() / stroke3.getVarBoundaryWidth() == 0.9)

		(t1, t2) = compoundConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)
		(t1, t2) = compoundConstraint2.intersections
		problem.appendConstraint(t2==0.5)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (48.75, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (206.25, 127.5))

		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (40, 235))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (215, 235))

	def testComponent_6(self):
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

		component.addCompoundConstraint(compoundConstraint1)
		component.addCompoundConstraint(compoundConstraint2)

		component.addCompoundConstraint(BoundaryConstraint(component, (40, 20, 215, 235)))

		problem = component.generateProblem()
		problem.appendConstraint(stroke3.getVarBoundaryWidth() / stroke1.getVarBoundaryWidth() == 0.9)

		(t1, t2) = compoundConstraint1.intersections
		problem.appendConstraint(t1==0.5)
		problem.appendConstraint(t2==0.5)
		(t1, t2) = compoundConstraint2.intersections
		problem.appendConstraint(t2==0.5)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (215, 127.5))

		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (48.75, 235))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (206.25, 235))

