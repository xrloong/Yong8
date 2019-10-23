from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import ConstraintComponent

from yong8.constraint import IntersectionPos
from yong8.constraint import SegmentIntersectionConstraint
from yong8.constraint import RawConstraint

from solver import Solver
# 十

strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()

stroke1 = strokeFactory.橫()
stroke2 = strokeFactory.豎()

component = componentFactory.generateComponent([stroke1, stroke2])

compoundConstraint1 = SegmentIntersectionConstraint(stroke1.getSegments()[0], stroke2.getSegments()[0])
compoundConstraint2 = RawConstraint(component.getVarBoundaryWidth() == stroke1.getVarBoundaryWidth())
compoundConstraint3 = RawConstraint(component.getVarBoundaryHeight() == stroke2.getVarBoundaryHeight())
component.addCompoundConstraint(compoundConstraint1)
component.addCompoundConstraint(compoundConstraint2)
component.addCompoundConstraint(compoundConstraint3)

problem = component.generateProblem()

(t1, t2) = compoundConstraint1.intersections
problem.appendConstraint(t1==0.5)
problem.appendConstraint(t2==0.5)
component.appendConstraintsWithBoundary(problem, (10, 10, 245, 245))

glyphSolver = Solver()
glyphSolver.solveProblem(problem)

print("Glyph: 十")
component.dump()

