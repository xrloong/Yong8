from yong8.drawing import DrawingGlyphPolicy
from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import LayoutConstraint
from yong8.component import ConstraintComponent
from yong8.component import IntersectionPos

from solver import Solver
# 十

strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()

stroke1 = strokeFactory.橫()
stroke2 = strokeFactory.豎()

component = componentFactory.generateComponent([stroke1, stroke2])

layoutConstraint1 = LayoutConstraint()
layoutConstraint1.setAsSegmentsIntersection(stroke1.getSegments()[0], stroke2.getSegments()[0])
layoutConstraint3 = LayoutConstraint()
layoutConstraint3.setAsRow(component.getVarBoundaryWidth() == stroke1.getVarBoundaryWidth())
layoutConstraint4 = LayoutConstraint()
layoutConstraint4.setAsRow(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())
component.appendLayoutConstraint(layoutConstraint1)
component.appendLayoutConstraint(layoutConstraint3)
component.appendLayoutConstraint(layoutConstraint4)


drawingGlyphPolicy = DrawingGlyphPolicy()
problem = component.generateProblem(drawingGlyphPolicy)

(t1, t2) = layoutConstraint1.intersections
problem.appendConstraint(t1==0.5)
problem.appendConstraint(t2==0.5)
component.appendConstraintsWithBoundary(problem, (10, 10, 245, 245))

glyphSolver = Solver()
glyphSolver.solveProblem(problem)

print("Glyph: 十")
for stroke in component.getStrokes():
    print("stroke:", stroke)
    print("start point:", stroke.getStartPoint())
    print("end point:", stroke.getEndPoint())
    print("")

