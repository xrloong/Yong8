from .base import BaseTestCase
from .base import GlyphSolver

from yong8.shape import ConstraintShape, ConstraintBoundaryShape
from yong8.drawing import DrawingGlyphPolicy

class ConstraintShapeTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testConstraintShape(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintShape)

class ConstraintBoundaryShapeTestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testConstraintBoundaryShape(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

class ConstraintBoundaryShape_Occupation_TestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testConstraintBoundaryShape(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

	def testConstraintBoundaryShape_constraintOccupationLeftTopRightBottom(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		problem.appendConstraint(shape.getVarOccupationBoundaryLeft()==38)
		problem.appendConstraint(shape.getVarOccupationBoundaryTop()==61)
		problem.appendConstraint(shape.getVarOccupationBoundaryRight()==182)
		problem.appendConstraint(shape.getVarOccupationBoundaryBottom()==129)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundary(), (38, 61, 182, 129))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110, 95))

	def testConstraintBoundaryShape_constraintOccupationSizeAndCenter(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		problem.appendConstraint(shape.getVarOccupationBoundaryWidth()==144)
		problem.appendConstraint(shape.getVarOccupationBoundaryHeight()==68)
		problem.appendConstraint(shape.getVarOccupationBoundaryCenterX()==110)
		problem.appendConstraint(shape.getVarOccupationBoundaryCenterY()==95)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getOccupationBoundary(), (38, 61, 182, 129))

	def testConstraintBoundaryShape_bindOccupationBoundary(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		shape.appendConstraintsWithOccupationBoundary(problem, (38, 61, 182, 129))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getOccupationSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getOccupationBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_bindOccupationSizeCenter(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		shape.appendConstraintsWithOccupationSizeCenter(problem, (144, 68), (110.0, 95.0))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getOccupationBoundary(), (38, 61, 182, 129))

class ConstraintBoundaryShape_Extension_TestCase(BaseTestCase):
	def setUp(self):
		super().setUp()

	def tearDown(self):
		super().tearDown()

	def testConstraintBoundaryShape(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

	def testConstraintBoundaryShape_constraintExtensionLeftTopRightBottom(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		problem.appendConstraint(shape.getVarExtensionBoundaryLeft()==38)
		problem.appendConstraint(shape.getVarExtensionBoundaryTop()==61)
		problem.appendConstraint(shape.getVarExtensionBoundaryRight()==182)
		problem.appendConstraint(shape.getVarExtensionBoundaryBottom()==129)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundary(), (38, 61, 182, 129))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundaryCenter(), (110, 95))

	def testConstraintBoundaryShape_constraintExtensionSizeAndCenter(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		problem.appendConstraint(shape.getVarExtensionBoundaryWidth()==144)
		problem.appendConstraint(shape.getVarExtensionBoundaryHeight()==68)
		problem.appendConstraint(shape.getVarExtensionBoundaryCenterX()==110)
		problem.appendConstraint(shape.getVarExtensionBoundaryCenterY()==95)

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionBoundary(), (38, 61, 182, 129))

	def testConstraintBoundaryShape_bindExtensionBoundary(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		shape.appendConstraintsWithExtensionBoundary(problem, (38, 61, 182, 129))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionSize(), (144, 68))
		self.assertSequenceAlmostEqual(shape.getExtensionBoundaryCenter(), (110.0, 95.0))

	def testConstraintBoundaryShape_bindExtensionSizeCenter(self):
		injector = self.getInjector()

		shape = injector.get(ConstraintBoundaryShape)

		drawingGlyphPolicy = injector.get(DrawingGlyphPolicy)
		problem = shape.generateProblem(drawingGlyphPolicy)
		shape.appendConstraintsWithExtensionSizeCenter(problem, (144, 68), (110.0, 95.0))

		glyphSolver = injector.get(GlyphSolver)
		glyphSolver.solveProblem(problem)

		self.assertSequenceAlmostEqual(shape.getExtensionBoundary(), (38, 61, 182, 129))

