# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:10:15 2019

@author: Guilherme Neumann
"""

import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
from scipy import stats
from statistics import Statistics_Calculator
class Oneway(Statistics_Calculator):
    def calculate_test(self):
        df=self.data.copy()
        anova=stats.f_oneway(*df.T.values)
        self.results.write("\nAnova to columns "+str(df.columns)+str(anova)+"\n")
        print("\nAnova to columns "+str(df.columns)+str(anova)+"\n")
        
        anova2=stats.f_oneway(*df.values)
        self.results.write("\nAnova to rows "+str(df.index)+str(anova2)+"\n")
        print("\nAnova o rows "+str(df.index)+str(anova2)+"\n")
        
        return (anova,anova2)