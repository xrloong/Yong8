#!/bin/sh
PYTHONPATH="solvers/gekko" python3 -m unittest discover -t . -s tests/test/ -p "test_*.py"

