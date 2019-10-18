class DrawingGlyphPolicy:
	def __init__(self):
		pass

	def getGlyphSize(self):
		return (255, 255)

	def getMarginHorizontal(self):
		return 40

	def getMarginVertical(self):
		return 20

class DrawingPolicy:
	def __init__(self):
		self.drawingGlyphPolicy = DrawingGlyphPolicy()

	def getDrawingGlyphPolicy(self):
		return self.drawingGlyphPolicy

