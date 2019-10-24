from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import ConstraintComponent

from yong8.constraint import AlignCenterConstraint
from yong8.constraint import BoundaryConstraint

from solver import Solver
# 一

strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()

stroke = strokeFactory.橫()
component = componentFactory.generateComponent([stroke])

compoundConstraint1 = AlignCenterConstraint(component, stroke)
component.addCompoundConstraint(compoundConstraint1)

component.addCompoundConstraint(BoundaryConstraint(component, (10, 10, 245, 245)))

problem = component.generateProblem()

glyphSolver = Solver()
glyphSolver.solveProblem(problem)

print("Glyph: 一")
component.dump()

