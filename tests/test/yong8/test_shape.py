from .base import BaseTestCase
from .base import GlyphSolver

from yong8.factory import ShapeFactory

from yong8.constraint import BoundaryConstraint

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

	def testConstraintBoundaryShape_bindSizeCenter(self):
		injector = self.getInjector()

		shapeFactory = injector.get(ShapeFactory)
		shape = shapeFactory.generateShape()

		problem = shape.generateProblem()
		shape.appendConstraintsWithSizeCenter(problem, (144, 68), (110.0, 95.0))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getBoundary(), (38, 61, 182, 129))

