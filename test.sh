#!/bin/sh
PYTHONPATH=xie/ python3 -m unittest discover -t . -s tests/test/ -p "test_*.py"

