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

	def testResolve(self):
		import uuid

		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)
		glyphFactory = injector.get(GlyphFactory)

		stroke1 = strokeFactory.橫()
		stroke2 = strokeFactory.豎()

		component1 = componentFactory.generateComponent([stroke1])
		component2 = componentFactory.generateComponent([stroke2])
		glyph = glyphFactory.generateGlyph([component1, component2])

		segment1 = stroke1.getSegments()[0]
		segment2 = stroke2.getSegments()[0]
		self.assertIs(glyph.resolve(segment1.getId()), segment1)
		self.assertIs(glyph.resolve(segment2.getId()), segment2)
		self.assertIsNone(glyph.resolve(uuid.uuid4()))

	def testGlyph_1(self):
		injector = self.getInjector()

		strokeFactory = injector.get(StrokeFactory)
		componentFactory = injector.get(ComponentFactory)
		glyphFactory = injector.get(GlyphFactory)
		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)

		size = drawingGlyphPolicy.getGlyphSize()
		marginHorizontal = drawingGlyphPolicy.getMarginHorizontal()
		marginVertical = drawingGlyphPolicy.getMarginVertical()

		stroke = strokeFactory.橫()
		component = componentFactory.generateComponent([stroke])
		glyph = glyphFactory.generateGlyph([component])

		problem = glyph.generateProblem()

		problem.appendConstraint(glyph.getVarBoundaryLeft() - 0 == marginHorizontal)
		problem.appendConstraint(glyph.getVarBoundaryTop() - 0 == marginVertical)
		problem.appendConstraint(size[0] - glyph.getVarBoundaryRight() == marginHorizontal)
		problem.appendConstraint(size[1] - glyph.getVarBoundaryBottom() == marginVertical)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getBoundary(), (40.0, 20.0, 215.0, 235.0))

	def testEmptyGlyph(self):
		injector = self.getInjector()

		glyphFactory = injector.get(GlyphFactory)
		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)

		size = drawingGlyphPolicy.getGlyphSize()
		marginHorizontal = drawingGlyphPolicy.getMarginHorizontal()
		marginVertical = drawingGlyphPolicy.getMarginVertical()

		glyph = glyphFactory.generateGlyph([])
		problem = glyph.generateProblem()

		problem.appendConstraint(glyph.getVarBoundaryLeft() - 0 == marginHorizontal)
		problem.appendConstraint(glyph.getVarBoundaryTop() - 0 == marginVertical)
		problem.appendConstraint(size[0] - glyph.getVarBoundaryRight() == marginHorizontal)
		problem.appendConstraint(size[1] - glyph.getVarBoundaryBottom() == marginVertical)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getBoundary(), (40.0, 20.0, 215.0, 235.0))

	def testGlyphMargin(self):
		injector = self.getInjector()

		glyphFactory = injector.get(GlyphFactory)
		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)

		size = drawingGlyphPolicy.getGlyphSize()
		marginHorizontal = drawingGlyphPolicy.getMarginHorizontal()
		marginVertical = drawingGlyphPolicy.getMarginVertical()

		glyph = glyphFactory.generateGlyph([])
		problem = glyph.generateProblem()

		problem.appendConstraint(glyph.getVarBoundaryLeft() - 0 == marginHorizontal)
		problem.appendConstraint(glyph.getVarBoundaryTop() - 0 == marginVertical)
		problem.appendConstraint(size[0] - glyph.getVarBoundaryRight() == marginHorizontal)
		problem.appendConstraint(size[1] - glyph.getVarBoundaryBottom() == marginVertical)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(glyph.getBoundary(), (40.0, 20.0, 215.0, 235.0))

