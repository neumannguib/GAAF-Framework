# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 13:37:34 2019

@author: Guilherme Neumann
"""

import unit_tests as ts

print('Testing quast')
test=ts.unit_tests()
test.Quast('/home/gneumann/gaef/unit_tests/tests/assemblies/spades/test1/scaffolds.fasta','pO113.fasta','tests')