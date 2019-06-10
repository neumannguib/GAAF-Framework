# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:08:49 2019

@author: Guilherme Neumann
"""

import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
import matplotlib.pyplot as plt 
import seaborn as sns; sns.set()
from statistics import Statistics_Calculator

class Correlation_pearson(Statistics_Calculator):
     
    def calculate_test(self):
        df=self.data.copy()
        df[self.var]=self.samples
        corr = df.corr(method='pearson')
        print(corr)
        sns.set(font_scale=1.2)
        sns.heatmap(corr, annot=True, fmt=".2f", linewidths=.5, cmap="RdBu")
        plt.xticks(rotation=90)
        fig = plt.gcf()
        fig.set_size_inches(12, 8)
        corr_file_name = self.out+'corr_'+self.metric
        fig.savefig(corr_file_name+self.run+'.png', dpi=300, bbox_inches='tight')
        fig.clear()	
        plt.clf()
        corr.to_csv(corr_file_name+'.csv', mode='w')
        return corr
    