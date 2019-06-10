# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:37:41 2019

@author: Guilherme Neumann
"""

import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
from statsmodels.stats.multicomp import (MultiComparison)
from scipy import stats
from statistics import Statistics_Calculator

class Bonferroni(Statistics_Calculator):
     
    def calculate_test(self):
        """It applies Holm-Bonferroni test to the dataframe. Bonferroni is a multi-comparison method.
        Discover more at https://en.wikipedia.org/wiki/Holm%E2%80%93Bonferroni_method .
        Be sure you are working with a normal distribution"""
        
        MultiComp = MultiComparison(self.data.values,self.data.index)
        holm=MultiComp.allpairtest(stats.ttest_rel, method='Holm')
        print("\nHolm-Bonferroni test for rows\n"+str(holm) +"\n")
        self.results.write("\nHolm-Bonferroni test for rows\n"+str(holm) +"\n")
        
        MultiComp = MultiComparison(self.data.T.values,self.data.columns)
        holm2=MultiComp.allpairtest(stats.ttest_rel, method='Holm')
        print("\nHolm-Bonferroni test for columns\n"+str(holm2) +"\n")
        self.results.write("\nHolm-Bonferroni test for columns\n"+str(holm2) +"\n")
        
        return (holm,holm2)
    