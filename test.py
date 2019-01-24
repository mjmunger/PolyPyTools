#!/usr/bin/env python3
import sys
from poly_py_tools.pw_strength_calculator import PasswordStrengthCalculator

Calc = PasswordStrengthCalculator(sys.argv[1])
Calc.verbosity = 1
print("Cracking improbable: %s " % "True" if Calc.evaluate() else "False")