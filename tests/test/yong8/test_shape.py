from .base import BaseTestCase

from yong8.shape import ConstraintShape, ConstraintBoundaryShape
from yong8.constants import GlyphSolver
from yong8.constants import DrawingSystem

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
		drawingSystem = injector.get(DrawingSystem)

		shape = injector.get(ConstraintBoundaryShape)

	def testConstraintBoundaryShape_BindingExtensionBoundary(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		shape = injector.get(ConstraintBoundaryShape)

		problem = shape.generateProblem(drawingSystem)
		shape.appendConstraintsWithExtensionBoundary(problem, (38, 61, 182, 129))

		drawingSystem.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundaryCenter(), (110.0, 95.0))
		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_BindingOccupationBoundary(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		shape = injector.get(ConstraintBoundaryShape)

		problem = shape.generateProblem(drawingSystem)
		shape.appendConstraintsWithExtensionBoundary(problem, (38, 61, 182, 129))

		drawingSystem.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundaryCenter(), (110.0, 95.0))
		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_BindingSizeCenter(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		shape = injector.get(ConstraintBoundaryShape)

		problem = shape.generateProblem(drawingSystem)
		shape.appendConstraintsWithExtensionBoundary(problem, (38, 61, 182, 129))

		drawingSystem.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundary(), (38, 61, 182, 129))
		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

