from injector import Module
from injector import provider

from yong8.drawing import DrawingPolicy
from yong8.drawing import DrawingGlyphPolicy

class DrawingModule(Module):
	@provider
	def provideDrawingPolicy(self) -> DrawingPolicy:
		return DrawingPolicy()

	@provider
	def provideDrawingGlyphPolicy(self) -> DrawingGlyphPolicy:
		return DrawingGlyphPolicy()

