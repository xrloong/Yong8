from injector import Module
from injector import provider

from .drawing import DrawingPolicy
from .drawing import DrawingGlyphPolicy

class DrawingModule(Module):
	@provider
	def provideDrawingPolicy(self) -> DrawingPolicy:
		return DrawingPolicy()

	@provider
	def provideDrawingGlyphPolicy(self) -> DrawingGlyphPolicy:
		return DrawingGlyphPolicy()

