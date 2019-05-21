# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:57:50 2019

@author: Guilherme Neumann
"""

from scipy import stats as stat
import logging 
import random
import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
import matplotlib.pyplot as plt 
import seaborn as sns; sns.set()
from statsmodels.stats.multicomp import (pairwise_tukeyhsd,MultiComparison)
import scikit_posthocs as sp
import pandas as pd
pd.set_option('display.max_colwidth', -1)

class Statistics:
    def __init__(self, data, exp,var, metric, out, samples,run=''):
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out + exp + '.log',level=logging.DEBUG)
        self.df=data
        self.exp=exp
        self.metric=metric
        self.out=out
        self.samples=samples
        self.var=var
        
        try:
            df=data.copy()
            self.results=open(out+"final_stats_"+metric+run+".txt","a")
            self.results.write(exp+" Statistics "+metric+":\n")
            print(exp+" Statistics "+metric+":\n")
            self.results.write("\nMean:\n"+df.mean().to_string()+"\n")
            print("\nMean:\n"+df.mean().to_string()+"\n")
            self.results.write(df.T.mean().to_string()+"\n")
            print(df.T.mean().to_string()+"\n")
            
            self.results.write("\nMedian:\n"+df.median().to_string()+"\n")
            print("\nMedian:\n"+df.median().to_string()+"\n")
            self.results.write(df.T.median().to_string()+"\n")
            print(df.T.median().to_string()+"\n")

            '''self.results.write("\nMode:\n"+df.mode().to_string()+"\n")
            print("\nMode:\n"+df.mode().to_string()+"\n")
            self.results.write(df.T.mode().to_string()+"\n")
            print(df.T.mode().to_string()+"\n")

            self.results.write("\nVariance:\n"+df.var().to_string()+"\n")
            print("\nVariance:\n"+df.var().to_string()+"\n")
            self.results.write(df.T.var().to_string()+"\n")
            print(df.T.var().to_string()+"\n")'''

            self.results.write("\nStandart deviation:\n"+df.std().to_string()+"\n")
            print("\nStandart deviation:\n"+df.std().to_string()+"\n")
            self.results.write(df.T.std().to_string()+"\n")
            print(df.T.std().to_string()+"\n")
            

            

        except IOError:
            print(IOError)
            logging.error(IOError)
            
    def scatter_plot(self,colors=[]):
        df=self.df.copy()
        samples=[]
        for one in self.samples:
            samples.append(int(one))
            
        df[self.var]=samples
        ax=[]
        if colors==[]:
            colors={assembler:["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]),random.choice('8*hPov^<>')] for assembler in df.columns}
        for column in df.columns:
            if column!=self.var:
                if ax!=[]:
                    ax.append(df.plot(kind='scatter',x=self.var,y=column,marker=colors[column][1],color=colors[column][0],label=column, ax=ax.pop()))
                else:
                    ax.append(df.plot(kind='scatter',x=self.var,y=column,marker=colors[column][1],color=colors[column][0],label=column))
        plt.ylabel(self.metric)
        plt.xticks(rotation=90)
        fig = plt.gcf()
        fig.set_size_inches(12, 8)
        fig.savefig(self.out+self.metric+'.png', dpi=300)
        fig.clear()
        
    def normality(self):
        self.results.write("\nNormality test (shapiro)\n")
        print("\nNormality test (shapiro)\n")
        norm_col=True
        for col in self.df.columns:
            x=stat.shapiro(self.df[col]) #if normal
            self.results.write(col+" "+str(x)+"\n")
            print(col+" "+str(x)+"\n")
            if x[1]<0.05:
                norm_col=False
        norm_index=True
        for col in self.df.index:
            x=stat.shapiro(self.df.T[col]) #if normal
            self.results.write(col+" "+str(x)+"\n")
            print(col+" "+str(x)+"\n")
            if x[1]<0.05:
                norm_index=False
        return(norm_col,norm_index)
    
    def kruskal(self):
        k=stat.kruskal(*self.df.T.values)
        self.results.write("\nKruskal to columns "+str(self.df.columns)+str(k)+"\n")
        print("\nKruskal to columns "+str(self.df.columns)+str(k)+"\n")
        
        k2=stat.kruskal(*self.df.values)
        self.results.write("\nKruskal to rows "+str(self.df.index)+str(k2)+"\n")
        print("\nKruskal to rows "+str(self.df.index)+str(k2)+"\n")
        
        return (k,k2)
    
    def oneway(self):
        anova=stat.f_oneway(*self.df.T.values)
        self.results.write("\nAnova to columns "+str(self.df.columns)+str(anova)+"\n")
        print("\nAnova to columns "+str(self.df.columns)+str(anova)+"\n")
        
        anova2=stat.f_oneway(*self.df.values)
        self.results.write("\nAnova to rows "+str(self.df.index)+str(anova2)+"\n")
        print("\nAnova o rows "+str(self.df.index)+str(anova2)+"\n")
        
        return (anova,anova2)
    
    
    def correlation_pearson(self):
        df=self.df.copy()
        df[self.var]=self.samples
        corr = df.corr(method='pearson')
        print(corr)
        sns.set(font_scale=1.2)
        sns.heatmap(corr, annot=True, fmt=".2f", linewidths=.5, cmap="RdBu")
        plt.xticks(rotation=90)
        fig = plt.gcf()
        fig.set_size_inches(12, 8)
        corr_file_name = self.out+'corr_'+self.metric
        fig.savefig(corr_file_name+'.png', dpi=300, bbox_inches='tight')
        fig.clear()	
        plt.clf()
        corr.to_csv(corr_file_name+'.csv', mode='w')
        return corr
    
    '''----------------------------------post-hoc tests-------------------------------------------------'''
    
    def tukey_test(self):
        """It applies Tukey test to the dataframe. Tukey is a multi-comparison method.
        Discover more at  https://en.wikipedia.org/wiki/Tukey’s_range_test .
        Be sure you are working with a normal distribution"""

        MultiComp = MultiComparison(self.df.values,self.df.index)
        tukey=MultiComp.tukeyhsd().summary()
        print("\nTukey test for rows\n"+str(tukey) +"\n")
        self.results.write("\nTukey test for rows\n"+str(tukey) +"\n")
        
        MultiComp = MultiComparison(self.df.T.values,self.df.columns)
        tukey2=MultiComp.tukeyhsd().summary()
        print("\nTukey test for columns\n"+str(tukey2) +"\n")
        self.results.write("\nTukey test for columns\n"+str(tukey2) +"\n")
        return (tukey,tukey2)
    
    def bonferroni_test(self):
        """It applies Holm-Bonferroni test to the dataframe. Bonferroni is a multi-comparison method.
        Discover more at https://en.wikipedia.org/wiki/Holm%E2%80%93Bonferroni_method .
        Be sure you are working with a normal distribution"""
        
        MultiComp = MultiComparison(self.df.values,self.df.index)
        holm=MultiComp.allpairtest(stat.ttest_rel, method='Holm')
        print("\nHolm-Bonferroni test for rows\n"+str(holm) +"\n")
        self.results.write("\nHolm-Bonferroni test for rows\n"+str(holm) +"\n")
        
        MultiComp = MultiComparison(self.df.T.values,self.df.columns)
        holm2=MultiComp.allpairtest(stat.ttest_rel, method='Holm')
        print("\nHolm-Bonferroni test for columns\n"+str(holm2) +"\n")
        self.results.write("\nHolm-Bonferroni test for columns\n"+str(holm2) +"\n")
        
        return (holm,holm2)
    
    def nemenyi_test(self):
        """It applies Nemenyi test to the dataframe. Nemenyi is a multi-comparison method.
        Discover more at https://www.pydoc.io/pypi/scikit-posthocs-0.3.7/autoapi/_posthocs/index.html .
        It is used to non-parametric data"""
        
        nem1=sp.posthoc_nemenyi(self.df.T.values)
        nem1.index=self.df.columns
        nem1.columns=self.df.columns
        print("\nNemenyi test for columns (p-value): \n")
        print(nem1)
        self.results.write("\nNemenyi test for columns (p-value):\n"+str(nem1) +"\n")
        
        nem2=sp.posthoc_nemenyi(self.df.values)
        nem2.index=self.df.index
        nem2.columns=self.df.index
        print("\nNemenyi test for rows (p-value):\n")
       
        print(nem2)
        self.results.write("\nNemenyi test for rows (p-value):\n"+str(nem2) +"\n")
        
        return (nem1,nem2)
    
    def linear_regression_all_samples(self):
        try:
            values=[]
            variables=[]
            df=self.df.copy()
            df=df.sort_index()
            for i,index in enumerate(df.index):
                val=df.loc[index]
                for va in val:
                    values.append(va)
                    variables.append(int(self.samples[i]))
            #print(values,variables)
            reg=stat.linregress(values,variables)
            self.results.write("\nAll samples to exp. variables "+str(reg)+"\n")
            print("\nAll samples to exp. variables "+str(reg)+"\n")
        except:
            print("Error in regression")
    
    def linear_regression(self):
        try:
            df=self.df.copy()
            df[self.var]=self.samples
            for column in df.columns:
                if column != self.var:
                    reg=stat.linregress(df[column],df[self.var])
                    self.results.write("\nLinear Regression to "+column+": "+str(reg)+"\n")
                    print("\nLinear Regression to "+column+": "+str(reg)+"\n")
        except:
            print("Error in regression")  
            
        
        
        