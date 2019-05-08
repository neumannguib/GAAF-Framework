# -*- coding: utf-8 -*-
"""
Created on Thu May  2 09:56:56 2019

@author: Guilherme Neumann
"""
import assembly
tools=assembly.Assembly(['reads100','reads150'], 'tests/', 'test', [100,150])
tools.k='77'
tools.run(["ssake","velvet", "abyss","edena","masurca","minia","mira","spades"])
#tools.run(["all"])