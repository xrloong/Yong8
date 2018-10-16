from injector import Module
from injector import provider

from .drawing import ConstraintDrawingSystem
from .constants import DrawingSystem
from .constants import GlyphSolver

class DrawingModule(Module):
	@provider
	def provideDrawingSystem(self, glyphSolver: GlyphSolver) -> DrawingSystem:
		return ConstraintDrawingSystem(glyphSolver)

