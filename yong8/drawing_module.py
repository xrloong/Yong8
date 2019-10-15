from injector import Module
from injector import provider

from .drawing import ConstraintDrawingSystem
from .drawing import DrawingPolicy
from .constants import DrawingSystem
from .constants import GlyphSolver

class DrawingModule(Module):
	@provider
	def provideDrawingSystem(self, glyphSolver: GlyphSolver, drawingPolicy: DrawingPolicy) -> DrawingSystem:
		return ConstraintDrawingSystem(glyphSolver, drawingPolicy)

	@provider
	def provideDrawingPolicy(self) -> DrawingPolicy:
		return DrawingPolicy()

