from .base import BaseTestCase
from .base import GlyphSolver

from yong8.drawing import DrawingGlyphPolicy
from yong8.factory import SegmentFactory
from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory
from yong8.factory import GlyphFactory

class ConstraintGlyphTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testGlyph_1(self):
		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)
		glyphFactory = injector.get(GlyphFactory)

		stroke = strokeFactory.橫()
		component = componentFactory.generateComponent([stroke])
		glyph = glyphFactory.generateGlyph([component])

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = glyph.generateProblem(drawingGlyphPolicy)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getBoundary(), (40.0, 20.0, 215.0, 235.0))

	def testEmptyGlyph(self):
		injector = self.getInjector()

		glyphFactory = injector.get(GlyphFactory)

		glyph = glyphFactory.generateGlyph([])

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = glyph.generateProblem(drawingGlyphPolicy)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(glyph.getMargin(), (40.0, 20.0, 215.0, 235.0))

	def testGlyphMargin(self):
		injector = self.getInjector()

		glyphFactory = injector.get(GlyphFactory)

		glyph = glyphFactory.generateGlyph([])

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = glyph.generateProblem(drawingGlyphPolicy)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getBoundary(), (40.0, 20.0, 215.0, 235.0))
		self.assertSequenceAlmostEqual(glyph.getMargin(), (40.0, 20.0, 215.0, 235.0))

