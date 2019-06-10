# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:55:18 2019

@author: Gui
"""

import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
import stats
from statistics import Statistics_Calculator


class Linear_regression(Statistics_Calculator):
     
    def calculate_test(self):
        try:
            df=self.data.copy()
            df[self.var]=self.samples
            for column in df.columns:
                if column != self.var:
                    reg=stats.linregress(df[column],df[self.var])
                    self.results.write("\nLinear Regression to "+column+": "+str(reg)+"\n")
                    print("\nLinear Regression to "+column+": "+str(reg)+"\n")
        except:
            print("Error in regression")  