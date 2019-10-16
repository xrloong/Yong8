from enum import Enum
from injector import Key

VariableGenerator = Key('VariableGenerator')
GlyphSolver = Key('GlyphSolver')
DrawingSystem = Key('DrawingSystem')

class Optimization(Enum):
	Maximize = 1
	Minimize = 2

