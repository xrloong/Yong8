from .base import BaseTestCase

from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.stroke import ConstraintStroke
from yong8.component import LayoutConstraint
from yong8.component import ConstraintComponent
from yong8.constants import GlyphSolver
from yong8.constants import DrawingSystem

class ConstraintComponentTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testComponent_1(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BeelineSegment_橫)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments([s]);
		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAlignCenter(stroke)

		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAsRow(component.getVarOccupationBoundaryWidth() == stroke.getVarOccupationBoundaryWidth())

		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsMinimize(component.getVarOccupationBoundaryHeight()*2)

		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)


		component.appendVariables(drawingSystem)
		component.appendConstraints(drawingSystem)
		component.appendObjective(drawingSystem)

		component.appendConstraintsWithBoundary(drawingSystem, (40, 20, 215, 235))
		drawingSystem.solve()

		self.assertSequenceAlmostEqual(component.getBoundary(), (40.0, 127.5, 215.0, 127.5))
		self.assertSequenceAlmostEqual(component.getSize(), (175, 0))
		self.assertSequenceAlmostEqual(stroke.getBoundary(), (40.0, 127.5, 215.0, 127.5))
		self.assertSequenceAlmostEqual(stroke.getSize(), (175, 0))
		self.assertSequenceAlmostEqual(stroke.getStartPoint(), (40, 127.5))
		self.assertSequenceAlmostEqual(stroke.getEndPoint(), (215, 127.5))

	def testComponent_2(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s1 = injector.get(BeelineSegment_橫)
		stroke1 = injector.get(ConstraintStroke)
		stroke1.setSegments([s1]);

		s2 = injector.get(BeelineSegment_豎)
		stroke2 = injector.get(ConstraintStroke)
		stroke2.setSegments([s2]);

		component = injector.get(ConstraintComponent)
		component.setStrokes([stroke1, stroke2])

		layoutConstraint1 = LayoutConstraint()
		layoutConstraint1.setAlignCenter(stroke1)
		layoutConstraint2 = LayoutConstraint()
		layoutConstraint2.setAlignCenter(stroke2)
		layoutConstraint3 = LayoutConstraint()
		layoutConstraint3.setAsRow(component.getVarOccupationBoundaryWidth() == stroke1.getVarOccupationBoundaryWidth())
		layoutConstraint4 = LayoutConstraint()
		layoutConstraint4.setAsRow(component.getVarOccupationBoundaryHeight() == stroke2.getVarOccupationBoundaryHeight())
		component.appendLayoutConstraint(layoutConstraint1)
		component.appendLayoutConstraint(layoutConstraint2)
		component.appendLayoutConstraint(layoutConstraint3)
		component.appendLayoutConstraint(layoutConstraint4)

		component.appendVariables(drawingSystem)
		component.appendConstraints(drawingSystem)
		component.appendObjective(drawingSystem)

		component.appendConstraintsWithBoundary(drawingSystem, (40, 20, 215, 235))
		drawingSystem.solve()

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

