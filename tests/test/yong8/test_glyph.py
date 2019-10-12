from .base import BaseTestCase

from yong8.segment import BaseConstraintBeelineSegment
from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.stroke import ConstraintStroke
from yong8.component import ConstraintComponent
from yong8.glyph import ConstraintGlyph
from yong8.constants import GlyphSolver
from yong8.constants import DrawingSystem

class ConstraintGlyphTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testGlyph_1(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		s = injector.get(BeelineSegment_橫)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments([s]);
		strokeGroup = injector.get(ConstraintComponent)
		strokeGroup.setStrokes([stroke])
		glyph = injector.get(ConstraintGlyph)
		glyph.setComponents([strokeGroup])

		problem = glyph.generateProblem(drawingSystem)
		drawingSystem.appendProblem(problem)

		drawingSystem.solve()

		self.assertSequenceAlmostEqual(glyph.getOccupationBoundary(), (40.0, 20.0, 215.0, 235.0))

	def testEmptyGlyph(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		glyph = injector.get(ConstraintGlyph)
		glyph.setComponents([])

		problem = glyph.generateProblem(drawingSystem)
		drawingSystem.appendProblem(problem)

		drawingSystem.solve()

		self.assertSequenceAlmostEqual(glyph.getOccupationBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(glyph.getMargin(), (40.0, 20.0, 215.0, 235.0))

	def testGlyphMargin(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		glyph = injector.get(ConstraintGlyph)
		glyph.setComponents([])

		problem = glyph.generateProblem(drawingSystem)
		drawingSystem.appendProblem(problem)

		drawingSystem.solve()

		self.assertSequenceAlmostEqual(glyph.getOccupationBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(glyph.getMargin(), (40.0, 20.0, 215.0, 235.0))

