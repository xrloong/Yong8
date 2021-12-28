from .shape import ConstraintBoundaryShape

from .segment import BaseConstraintBeelineSegment
from .segment import BaseConstraintQCurveSegment

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
		return BaseConstraintBeelineSegment([-1, -1])

	def generateBeelineSegment_N0(self):
		return BaseConstraintBeelineSegment([-1, 0])

	def generateBeelineSegment_NP(self):
		return BaseConstraintBeelineSegment([-1, 1])

	def generateBeelineSegment_0N(self):
		return BaseConstraintBeelineSegment([0, 1])

	def generateBeelineSegment_00(self):
		return BaseConstraintBeelineSegment([0, 0])

	def generateBeelineSegment_0P(self):
		return BaseConstraintBeelineSegment([0, 1])

	def generateBeelineSegment_PN(self):
		return BaseConstraintBeelineSegment([1, -1])

	def generateBeelineSegment_P0(self):
		return BaseConstraintBeelineSegment([1, 0])

	def generateBeelineSegment_PP(self):
		return BaseConstraintBeelineSegment([1, 1])

	def generateBeelineSegment_橫(self):
		return BaseConstraintBeelineSegment([1, 0])

	def generateBeelineSegment_豎(self):
		return BaseConstraintBeelineSegment([0, 1])

class StrokeFactory:
	def __init__(self):
		self.segmentFactory = SegmentFactory()

	def generateStroke(self, segments, weights = None):
		return ConstraintStroke(segments, weights)

	def 提(self):
		raise NotImplementedError('提() is not implemented yet')

	def 彎鉤(self):
		raise NotImplementedError('彎鉤() is not implemented yet')

	def 斜鉤(self):
		raise NotImplementedError('斜鉤() is not implemented yet')

	def 扁斜鉤(self):
		raise NotImplementedError('扁斜鉤() is not implemented yet')

	def 豎彎(self):
		raise NotImplementedError('豎彎() is not implemented yet')

	def 橫折鉤(self):
		raise NotImplementedError('橫折鉤() is not implemented yet')

	def 橫撇(self):
		raise NotImplementedError('橫撇() is not implemented yet')

	def 橫折彎鉤(self):
		raise NotImplementedError('橫折彎鉤() is not implemented yet')

	def 豎折彎鉤(self):
		raise NotImplementedError('豎折彎鉤() is not implemented yet')

	def 橫折提(self):
		raise NotImplementedError('橫折提() is not implemented yet')

	def 橫折折撇(self):
		raise NotImplementedError('橫折折撇() is not implemented yet')

	def 橫撇彎鉤(self):
		raise NotImplementedError('橫撇彎鉤() is not implemented yet')

	def 橫折彎(self):
		raise NotImplementedError('橫折彎() is not implemented yet')

	def 橫折折折(self):
		raise NotImplementedError('橫折折折() is not implemented yet')


	def 捺(self):
		raise NotImplementedError('捺() is not implemented yet')

	def 橫(self):
		s = self.segmentFactory.generateBeelineSegment_橫()
		return self.generateStroke([s])

	def 豎(self):
		s = self.segmentFactory.generateBeelineSegment_豎()
		return self.generateStroke([s])

	def 撇(self):
		raise NotImplementedError('撇() is not implemented yet')

	def 豎撇(self):
		raise NotImplementedError('豎撇() is not implemented yet')

	def 點(self):
		raise NotImplementedError('點() is not implemented yet')

	def 橫折(self):
		s1 = self.segmentFactory.generateBeelineSegment_橫()
		s2 = self.segmentFactory.generateBeelineSegment_豎()
		return self.generateStroke([s1, s2])

	def 橫鉤(self):
		raise NotImplementedError('橫鉤() is not implemented yet')

	def 豎折(self):
		raise NotImplementedError('豎折() is not implemented yet')

	def 豎彎左(self):
		raise NotImplementedError('豎彎左() is not implemented yet')

	def 豎提(self):
		raise NotImplementedError('豎提() is not implemented yet')

	def 豎鉤(self):
		raise NotImplementedError('豎鉤() is not implemented yet')

	def 撇點(self):
		raise NotImplementedError('撇點() is not implemented yet')

	def 撇折(self):
		raise NotImplementedError('撇折() is not implemented yet')

	def 提捺(self):
		raise NotImplementedError('提捺() is not implemented yet')

	def 豎折折(self):
		raise NotImplementedError('豎折折() is not implemented yet')

	def 豎彎鉤(self):
		raise NotImplementedError('豎彎鉤() is not implemented yet')

	def 橫斜彎鉤(self):
		raise NotImplementedError('橫斜彎鉤() is not implemented yet')

	def 橫折折折鉤(self):
		raise NotImplementedError('橫折折折鉤() is not implemented yet')

	def 撇鉤(self):
		raise NotImplementedError('撇鉤() is not implemented yet')

	def 圈(self):
		raise NotImplementedError('圈() is not implemented yet')

class ComponentFactory:
	def generateComponent(self, strokes):
		component = ConstraintComponent(strokes)
		return component

class GlyphFactory:
	def generateGlyph(self, components):
		glyph = ConstraintGlyph(components)
		return glyph

