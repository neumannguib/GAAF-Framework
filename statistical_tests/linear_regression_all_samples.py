# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:01:39 2019

@author: Guilherme Neumann
"""

import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
import stats
from statistics import Statistics_Calculator


class Linear_regression_all_samples(Statistics_Calculator):
     
    def calculate_test(self):
        try:
            values=[]
            variables=[]
            df=self.data.copy()
            df=df.sort_index()
            for i,index in enumerate(df.index):
                val=df.loc[index]
                for va in val:
                    values.append(va)
                    variables.append(int(self.samples[i]))
            #print(values,variables)
            reg=stats.linregress(values,variables)
            self.results.write("\nAll samples to exp. variables "+str(reg)+"\n")
            print("\nAll samples to exp. variables "+str(reg)+"\n")
        except:
            print("Error in regression")