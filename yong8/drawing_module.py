from injector import Module
from injector import provider

from .drawing import ConstraintDrawingSystem
from .constants import DrawingSystem
from .constants import VariableGenerator, GlyphSolver

class DrawingModule(Module):
	@provider
	def provideVariableGenerator(self, glyphSolver: GlyphSolver) -> VariableGenerator:
		return glyphSolver.getVariableGenerator()

	@provider
	def provideDrawingSystem(self, glyphSolver: GlyphSolver) -> DrawingSystem:
		return ConstraintDrawingSystem(glyphSolver)

