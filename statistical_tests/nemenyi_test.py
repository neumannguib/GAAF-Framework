# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:07:57 2019

@author: Guilherme Neumann
"""
import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
import scikit_posthocs as sp
from statistics import Statistics_Calculator


class Nemenyi_test(Statistics_Calculator):
     
    def calculate_test(self):
        """It applies Nemenyi test to the dataframe. Nemenyi is a multi-comparison method.
        Discover more at https://www.pydoc.io/pypi/scikit-posthocs-0.3.7/autoapi/_posthocs/index.html .
        It is used to non-parametric data"""
        
        nem1=sp.posthoc_nemenyi(self.df.T.values)
        nem1.index=self.df.columns
        nem1.columns=self.df.columns
        print("\nNemenyi test for columns (p-value): \n")
        print(nem1)
        #self.results.write("\nNemenyi test for columns (p-value):\n"+str(nem1) +"\n")
        nem1.to_csv("nem_columns_"+self.metric+"_"+self.run+".csv")
        nem2=sp.posthoc_nemenyi(self.df.values)
        nem2.index=self.df.index
        nem2.columns=self.df.index
        print("\nNemenyi test for rows (p-value):\n")
        nem2.to_csv("nem_rows_"+self.metric+"_"+self.run+".csv")
        print(nem2)
        #self.results.write("\nNemenyi test for rows (p-value):\n"+str(nem2) +"\n")
        
        return (nem1,nem2)
