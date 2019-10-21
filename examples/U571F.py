from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import LayoutConstraint
from yong8.component import ConstraintComponent
from yong8.component import IntersectionPos

from solver import Solver
# 土

strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()

stroke = strokeFactory.橫()
component = componentFactory.generateComponent([stroke])

stroke1 = strokeFactory.橫()
stroke2 = strokeFactory.豎()
stroke3 = strokeFactory.橫()

component = componentFactory.generateComponent([stroke1, stroke2, stroke3])

layoutConstraint1 = LayoutConstraint()
layoutConstraint1.setAsSegmentsIntersection(stroke1.getSegments()[0], stroke2.getSegments()[0])
layoutConstraint2 = LayoutConstraint()
layoutConstraint2.setAsSegmentsIntersection(stroke2.getSegments()[0], stroke3.getSegments()[0], IntersectionPos.End, IntersectionPos.BetweenStartEnd)
layoutConstraint3 = LayoutConstraint()
layoutConstraint3.setAsRow(component.getVarBoundaryWidth() == stroke3.getVarBoundaryWidth())
layoutConstraint4 = LayoutConstraint()
layoutConstraint4.setAsRow(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())
component.appendLayoutConstraint(layoutConstraint1)
component.appendLayoutConstraint(layoutConstraint2)
component.appendLayoutConstraint(layoutConstraint3)
component.appendLayoutConstraint(layoutConstraint4)



problem = component.generateProblem()
problem.appendConstraint(stroke1.getVarBoundaryWidth() / stroke3.getVarBoundaryWidth() == 0.9)

(t1, t2) = layoutConstraint1.intersections
problem.appendConstraint(t1==0.5)
problem.appendConstraint(t2==0.5)
(t1, t2) = layoutConstraint2.intersections
problem.appendConstraint(t2==0.5)
component.appendConstraintsWithBoundary(problem, (10, 10, 245, 245))

glyphSolver = Solver()
glyphSolver.solveProblem(problem)

print("Glyph: 土")
component.dump()

