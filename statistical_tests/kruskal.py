# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:11:27 2019

@author: Guilherme Neumann
"""

import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
from scipy import stats
from statistics import Statistics_Calculator
class Kruskal(Statistics_Calculator):
    def calculate_test(self):
        df=self.data.copy()
        k=stats.kruskal(*df.T.values)
        self.results.write("\nKruskal to columns "+str(df.columns)+str(k)+"\n")
        print("\nKruskal to columns "+str(df.columns)+str(k)+"\n")
        
        k2=stats.kruskal(*df.values)
        self.results.write("\nKruskal to rows "+str(df.index)+str(k2)+"\n")
        print("\nKruskal to rows "+str(df.index)+str(k2)+"\n")
        
        return (k,k2)