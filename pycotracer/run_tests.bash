# Name: run_tests.bash
# Desc: Runs the python unit tests for the pycotracer Colorado Tracer access
#       layer microlibrary.
# Auth: A. Samuel Pottinger (Gleap LLC, 2013)
# Licn: GNU GPL v3

python -m unittest discover --pattern=*_test.py