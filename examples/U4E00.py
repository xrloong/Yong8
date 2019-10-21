from yong8.factory import StrokeFactory
from yong8.factory import ComponentFactory

from yong8.component import LayoutConstraint
from yong8.component import ConstraintComponent

from solver import Solver
# 一

strokeFactory = StrokeFactory()
componentFactory = ComponentFactory()

stroke = strokeFactory.橫()
component = componentFactory.generateComponent([stroke])

layoutConstraint1 = LayoutConstraint()
layoutConstraint1.setAsAlignCenter(stroke)

layoutConstraint2 = LayoutConstraint()
layoutConstraint2.setAsRow(component.getVarBoundaryWidth() == stroke.getVarBoundaryWidth())

layoutConstraint3 = LayoutConstraint()
layoutConstraint3.setAsMinimize(component.getVarBoundaryHeight()*2)

component.appendLayoutConstraint(layoutConstraint1)
component.appendLayoutConstraint(layoutConstraint2)
component.appendLayoutConstraint(layoutConstraint3)


problem = component.generateProblem()
component.appendConstraintsWithBoundary(problem, (10, 10, 245, 245))

glyphSolver = Solver()
glyphSolver.solveProblem(problem)

print("Glyph: 一")
component.dump()

