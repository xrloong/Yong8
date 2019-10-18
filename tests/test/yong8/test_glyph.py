from .base import BaseTestCase
from .base import GlyphSolver

from yong8.segment import BaseConstraintBeelineSegment
from yong8.segment import BeelineSegment_橫, BeelineSegment_豎
from yong8.stroke import ConstraintStroke
from yong8.component import ConstraintComponent
from yong8.glyph import ConstraintGlyph
from yong8.drawing import DrawingGlyphPolicy

class ConstraintGlyphTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testGlyph_1(self):
		injector = self.getInjector()

		s = injector.get(BeelineSegment_橫)
		stroke = injector.get(ConstraintStroke)
		stroke.setSegments([s]);
		strokeGroup = injector.get(ConstraintComponent)
		strokeGroup.setStrokes([stroke])
		glyph = injector.get(ConstraintGlyph)
		glyph.setComponents([strokeGroup])


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = glyph.generateProblem(drawingGlyphPolicy)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getOccupationBoundary(), (40.0, 20.0, 215.0, 235.0))

	def testEmptyGlyph(self):
		injector = self.getInjector()

		glyph = injector.get(ConstraintGlyph)
		glyph.setComponents([])


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = glyph.generateProblem(drawingGlyphPolicy)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getOccupationBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(glyph.getMargin(), (40.0, 20.0, 215.0, 235.0))

	def testGlyphMargin(self):
		injector = self.getInjector()

		glyph = injector.get(ConstraintGlyph)
		glyph.setComponents([])


		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = glyph.generateProblem(drawingGlyphPolicy)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getOccupationBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(glyph.getMargin(), (40.0, 20.0, 215.0, 235.0))

