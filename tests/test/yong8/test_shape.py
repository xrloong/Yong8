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

		shape.appendVariables(drawingSystem)
		shape.appendConstraints(drawingSystem)
		shape.appendConstraintsWithExtensionBoundary(drawingSystem, (38, 61, 182, 129))
		shape.appendObjective(drawingSystem)

		drawingSystem.solve()

		self.assertEqual(shape.getExtensionSize(), (144, 68))
		self.assertEqual(shape.getExtensionBoundaryCenter(), (110.0, 95.0))
		self.assertEqual(shape.getOccupationSize(), (144, 68))
		self.assertEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_BindingOccupationBoundary(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)

		shape = injector.get(ConstraintBoundaryShape)

		shape.appendVariables(drawingSystem)
		shape.appendConstraints(drawingSystem)
		shape.appendConstraintsWithOccupationBoundary(drawingSystem, (38, 61, 182, 129))
		shape.appendObjective(drawingSystem)

		drawingSystem.solve()

		self.assertEqual(shape.getExtensionSize(), (144, 68))
		self.assertEqual(shape.getExtensionBoundaryCenter(), (110.0, 95.0))
		self.assertEqual(shape.getOccupationSize(), (144, 68))
		self.assertEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_BindingSizeCenter(self):
		injector = self.getInjector()
		drawingSystem = injector.get(DrawingSystem)
		drawingSystem = drawingSystem.getGlyphSolver()

		shape = injector.get(ConstraintBoundaryShape)

		shape.appendVariables(drawingSystem)
		shape.appendConstraints(drawingSystem)
		shape.appendConstraintsWithSizeCenter(drawingSystem, (144, 68), (110, 95))
		shape.appendObjective(drawingSystem)

		drawingSystem.solve()

		self.assertEqual(shape.getExtensionSize(), (144, 68))
		self.assertEqual(shape.getExtensionBoundary(), (38, 61, 182, 129))
		self.assertEqual(shape.getOccupationSize(), (144, 68))
		self.assertEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

