from enum import Enum
from injector import Key

GlyphSolver = Key('GlyphSolver')

class Optimization(Enum):
	Maximize = 1
	Minimize = 2

