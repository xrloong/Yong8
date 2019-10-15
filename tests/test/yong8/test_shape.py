from .base import BaseTestCase

from yong8.shape import ConstraintShape, ConstraintBoundaryShape
from yong8.constants import GlyphSolver
from yong8.constants import DrawingSystem
from yong8.drawing import DrawingPolicy

class ConstraintShapeTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testConstraintShape(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintShape)

	def testConstraintBoundaryShape(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

	def testConstraintBoundaryShape_BindingExtensionBoundary(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		shape = injector.get(ConstraintBoundaryShape)

		problem = shape.generateProblem(drawingPolicy)
		shape.appendConstraintsWithExtensionBoundary(problem, (38, 61, 182, 129))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundaryCenter(), (110.0, 95.0))
		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_BindingOccupationBoundary(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		shape = injector.get(ConstraintBoundaryShape)

		problem = shape.generateProblem(drawingPolicy)
		shape.appendConstraintsWithExtensionBoundary(problem, (38, 61, 182, 129))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundaryCenter(), (110.0, 95.0))
		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_BindingSizeCenter(self):
		injector = self.getInjector()

		drawingPolicy = injector.get(DrawingPolicy)
		shape = injector.get(ConstraintBoundaryShape)

		problem = shape.generateProblem(drawingPolicy)
		shape.appendConstraintsWithExtensionBoundary(problem, (38, 61, 182, 129))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundary(), (38, 61, 182, 129))
		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

