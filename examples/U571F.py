from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import ConstraintComponent

from yong8.constraint import IntersectionPos
from yong8.constraint import SegmentIntersectionConstraint

from solver import Solver
# 土

strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()

stroke1 = strokeFactory.橫()
stroke2 = strokeFactory.豎()
stroke3 = strokeFactory.橫()

component = componentFactory.generateComponent([stroke1, stroke2, stroke3])

compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0])
compoundConstraint2 = SegmentIntersectionConstraint(stroke2.getSegments()[0], stroke3.getSegments()[0], IntersectionPos.End, IntersectionPos.BetweenStartEnd)
component.addCompoundConstraint(compoundConstraint1)
component.addCompoundConstraint(compoundConstraint2)

problem = component.generateProblem()
problem.appendConstraint(stroke1.getVarBoundaryWidth() / stroke3.getVarBoundaryWidth() == 0.9)

(t1, t2) = compoundConstraint1.intersections
problem.appendConstraint(t1==0.5)
problem.appendConstraint(t2==0.5)
(t1, t2) = compoundConstraint2.intersections
problem.appendConstraint(t2==0.5)
component.appendConstraintsWithBoundary(problem, (10, 10, 245, 245))

glyphSolver = Solver()
glyphSolver.solveProblem(problem)

print("Glyph: 土")
component.dump()

