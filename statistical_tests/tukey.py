# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:36:20 2019

@author: Guilherme Neumann
"""

import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
import scikit_posthocs as sp
import numpy as np
from statistics import Statistics_Calculator

class Tukey(Statistics_Calculator):
     
    def calculate_test(self):
        """It applies Tukey test to the dataframe. Tukey is a multi-comparison method.
        Discover more at  https://en.wikipedia.org/wiki/Tukey’s_range_test .
        Be sure you are working with a normal distribution"""

        
        g=[]
        for col in self.data.columns:
            g.append([col] * self.data.shape[0])
        tukey1=sp.posthoc_tukey_hsd(self.data.T,np.concatenate(g))
        print("\nNemenyi test for columns (p-value): \n")
        print(tukey1)
        #self.results.write("\nNemenyi test for columns (p-value):\n"+str(nem1) +"\n")
        tukey1.to_csv("outputs_csv/tukey_columns_"+self.metric+"_"+self.run+".csv")
        g=[]
        for col in self.df.index:
            g.append([col] * self.data.shape[1])
        tukey2=sp.posthoc_tukey_hsd(self.data,np.concatenate(g))
        print("\nNemenyi test for rows (p-value):\n")
        tukey2.to_csv("outputs_csv/tukey_rows_"+self.metric+"_"+self.run+".csv")
        print(tukey2)