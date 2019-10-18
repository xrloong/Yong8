from .shape import ConstraintBoundaryShape

from .segment import BaseConstraintBeelineSegment
from .segment import BaseConstraintQCurveSegment
from .segment import BeelineSegment_NN, BeelineSegment_N0, BeelineSegment_NP
from .segment import BeelineSegment_0N, BeelineSegment_00, BeelineSegment_0P
from .segment import BeelineSegment_PN, BeelineSegment_P0, BeelineSegment_PP
from .segment import BeelineSegment_橫, BeelineSegment_豎

from .stroke import ConstraintStroke

from .component import ConstraintComponent

from .glyph import ConstraintGlyph

class ShapeFactory:
	def generateShape(self):
		return ConstraintBoundaryShape()

class SegmentFactory:
	def generateBeelineSegment(self, dirConfig):
		segment = BaseConstraintBeelineSegment()
		segment.setDirConfig(dirConfig)
		return segment

	def generateBeelineSegment_NN(self):
		return BeelineSegment_NN()

	def generateBeelineSegment_N0(self):
		return BeelineSegment_N0()

	def generateBeelineSegment_NP(self):
		return BeelineSegment_NP()

	def generateBeelineSegment_0N(self):
		return BeelineSegment_0N()

	def generateBeelineSegment_00(self):
		return BeelineSegment_00()

	def generateBeelineSegment_0P(self):
		return BeelineSegment_0P()

	def generateBeelineSegment_PN(self):
		return BeelineSegment_PN()

	def generateBeelineSegment_P0(self):
		return BeelineSegment_P0()

	def generateBeelineSegment_PP(self):
		return BeelineSegment_PP()

	def generateBeelineSegment_橫(self):
		return BeelineSegment_橫()

	def generateBeelineSegment_豎(self):
		return BeelineSegment_豎()

class StrokeFactory:
	def __init__(self):
		pass

	def generateStroke(self, segments, weights = None):
		stroke = ConstraintStroke()
		stroke.setSegments(segments, weights)
		return stroke

class ComponentFactory:
	def generateComponent(self, strokes):
		component = ConstraintComponent()
		component.setStrokes(strokes)
		return component

class GlyphFactory:
	def generateGlyph(self, components):
		glyph = ConstraintGlyph()
		glyph.setComponents(components)
		return glyph

