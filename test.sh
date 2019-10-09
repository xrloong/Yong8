#!/bin/sh
PYTHONPATH="solvers/cvxpy" python3 -m unittest discover -t . -s tests/test/ -p "test_*.py"

