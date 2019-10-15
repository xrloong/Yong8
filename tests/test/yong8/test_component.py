from .base import BaseTestCase

from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.stroke import ConstraintStroke
from yong8.component import LayoutConstraint
from yong8.component import ConstraintComponent
from yong8.constants import GlyphSolver
from yong8.drawing import DrawingPolicy

class ConstraintComponentTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testComponent_1(self):
		# 一

		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
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

		problem = component.generateProblem(drawingPolicy)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(component.getBoundary(), (40.0, 127.5, 215.0, 127.5))
		self.assertSequenceAlmostEqual(component.getSize(), (175, 0))
		self.assertSequenceAlmostEqual(stroke.getBoundary(), (40.0, 127.5, 215.0, 127.5))
		self.assertSequenceAlmostEqual(stroke.getSize(), (175, 0))
		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (215, 127.5))

	def testComponent_2(self):
		# 十

		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
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

		problem = component.generateProblem(drawingPolicy)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(component.getBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(component.getSize(), (175.0, 215.0))
		self.assertSequenceAlmostEqual(stroke1.getBoundary(), (40.0, 127.5, 215.0, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getSize(), (175, 0))
		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (215, 127.5))
		self.assertSequenceAlmostEqual(stroke2.getBoundary(), (127.5, 20.0, 127.5, 235.0))
		self.assertSequenceAlmostEqual(stroke2.getSize(), (0, 215))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (127.5, 20))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (127.5, 235))

	def testComponent_3(self):
		# 口

		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
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

		problem = component.generateProblem(drawingPolicy)
		component.appendConstraintsWithBoundary(problem, (40, 20, 215, 235))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(component.getBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(component.getSize(), (175.0, 215.0))

		self.assertSequenceAlmostEqual(stroke1.getBoundary(), (40.0, 20.0, 40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke1.getSize(), (0.0, 215.0))
		self.assertSequenceAlmostEqual(stroke1.getStartPoint(), (40.0, 20.0))
		self.assertSequenceAlmostEqual(stroke1.getEndPoint(), (40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke2.getBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(stroke2.getSize(), (175.0, 215.0))
		self.assertSequenceAlmostEqual(stroke2.getStartPoint(), (40.0, 20.0))
		self.assertSequenceAlmostEqual(stroke2.getEndPoint(), (215.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getBoundary(), (40.0, 235.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getSize(), (175.0, 0.0))
		self.assertSequenceAlmostEqual(stroke3.getStartPoint(), (40.0, 235.0))
		self.assertSequenceAlmostEqual(stroke3.getEndPoint(), (215.0, 235.0))

