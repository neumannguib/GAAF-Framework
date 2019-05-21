# -*- coding: utf-8 -*-
"""
Created on Thu May  2 09:56:56 2019

@author: Guilherme Neumann
"""
import assembly
tools=assembly.Assembling_Control(['read_len_100','read_len_150'], "/home/gneumann/gaaf/unit_tests/tests/", 'test', [100,150])
tools.k='77'
#tools.run(["ssake","velvet", "abyss","edena","masurca","minia","mira","spades"])
tools.run(["ssake","velvet", "abyss"])
tools.run(["all"])