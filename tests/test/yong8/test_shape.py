from .base import BaseTestCase
from .base import GlyphSolver
from yong8.factory import ShapeFactory
from yong8.shape import PathParams

from yong8.constraint import BoundaryConstraint

class PathParamsTestCase(BaseTestCase):
	def testDefaultValues(self):
		pathParams = PathParams()

		self.assertEqual(pathParams.getWeights(), (0, 0))
		self.assertEqual(pathParams.getRangeWeightStartX(), 0)
		self.assertEqual(pathParams.getRangeWeightEndX(), 0)
		self.assertEqual(pathParams.getRangeWeightMaxX(), 0)
		self.assertEqual(pathParams.getRangeWeightStartY(), 0)
		self.assertEqual(pathParams.getRangeWeightEndY(), 1)
		self.assertEqual(pathParams.getRangeWeightMaxY(), 0)

	def testSetWeights(self):
		pathParams = PathParams()

		pathParams.setWidthWeight(2)
		pathParams.setHeightWeight(3)

		self.assertEqual(pathParams.getWeights(), (2, 3))

	def testSetRangeWeightX(self):
		pathParams = PathParams()

		pathParams.setRangeWeightX(0.25, 0.75)

		self.assertEqual(pathParams.getRangeWeightStartX(), 0.25)
		self.assertEqual(pathParams.getRangeWeightEndX(), 0.75)
		self.assertEqual(pathParams.getRangeWeightMaxX(), 1)

	def testSetRangeWeightY(self):
		pathParams = PathParams()

		pathParams.setRangeWeightY(0.5, 2, 4)

		self.assertEqual(pathParams.getRangeWeightStartY(), 0.5)
		self.assertEqual(pathParams.getRangeWeightEndY(), 2)
		self.assertEqual(pathParams.getRangeWeightMaxY(), 4)

	def testSetRangeWeightOutOfRange(self):
		pathParams = PathParams()

		with self.assertRaises(AssertionError):
			pathParams.setRangeWeightX(2, 0)
		with self.assertRaises(AssertionError):
			pathParams.setRangeWeightX(0, 2)
		with self.assertRaises(AssertionError):
			pathParams.setRangeWeightY(-1, 0)
		with self.assertRaises(AssertionError):
			pathParams.setRangeWeightY(0, -1)

class ConstraintBoundaryShape_TestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testInjector(self):
		injector = self.getInjector()
		self.assertIsNotNone(injector)

	def testInjectShapeFactory(self):
		injector = self.getInjector()
		shapeFactory = injector.get(ShapeFactory)
		self.assertIsNotNone(shapeFactory)

	def testConstraintBoundaryShape(self):
		injector = self.getInjector()
		shapeFactory = injector.get(ShapeFactory)
		shape = shapeFactory.generateShape()
		self.assertIsNotNone(shape)

	def testConstraintBoundaryShape_constraintLeftTopRightBottom(self):
		injector = self.getInjector()

		shapeFactory = injector.get(ShapeFactory)
		shape = shapeFactory.generateShape()

		problem = shape.generateProblem()
		problem.appendConstraint(shape.getVarBoundaryLeft()==38)
		problem.appendConstraint(shape.getVarBoundaryTop()==61)
		problem.appendConstraint(shape.getVarBoundaryRight()==182)
		problem.appendConstraint(shape.getVarBoundaryBottom()==129)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getBoundary(), (38, 61, 182, 129))
		self.assertSequenceAlmostEqual(shape.getBoundaryCenter(), (110, 95))

	def testConstraintBoundaryShape_constraintSizeAndCenter(self):
		injector = self.getInjector()

		shapeFactory = injector.get(ShapeFactory)
		shape = shapeFactory.generateShape()

		problem = shape.generateProblem()
		problem.appendConstraint(shape.getVarBoundaryWidth()==144)
		problem.appendConstraint(shape.getVarBoundaryHeight()==68)
		problem.appendConstraint(shape.getVarBoundaryCenterX()==110)
		problem.appendConstraint(shape.getVarBoundaryCenterY()==95)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getBoundary(), (38, 61, 182, 129))

	def testConstraintBoundaryShape_bindBoundary(self):
		injector = self.getInjector()

		shapeFactory = injector.get(ShapeFactory)
		shape = shapeFactory.generateShape()

		shape.addCompoundConstraint(BoundaryConstraint(shape, (38, 61, 182, 129)))

		problem = shape.generateProblem()

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getBoundaryCenter(), (110.0, 95.0))

