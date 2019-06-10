# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:57:50 2019

@author: Guilherme Neumann
"""

from scipy import stats
import logging 
import random
import matplotlib as mpl
mpl.use('Agg') #do not use display (to run in servers)
import matplotlib.pyplot as plt 
import seaborn as sns; sns.set()
import pandas as pd
import importlib
from abc import ABC, abstractmethod
pd.set_option('display.max_colwidth', -1)


class Statistics_Controller:
    """
    Class responsable for controlling statistical tests
    
    Attributes
    ----------
    df : DataFrame
        Dataframe cotaining all results for a certain feature/metric
    exp : str
        Experiment name
    metric : str
        Metric/feature name
    out : str
        Path to store outputs and where assemblies are stored
    samples : list
        list with sample names
    var : str
        The experiment variable
    run : str
        Run name or number, in case more than one 
        
    Methods
    -------
    mean()
        Calculates mean
    median()
        Calculates median
    standard_deviation()
        Calculates standard deviation
    scatter_plot(colors=[])
        Save a scatter plot to a figure
    normality()
        Tests normality through Shapiro
    test_hypothesis(test)
        Tests a hypothesis
    graph(graph_type)
        Create a graph
    create_report()
        Generate a report
     
    
    """
    def __init__(self, data, exp,var, metric, out, samples,run=''):
        """
        Parameters
        ----------
        data : DataFrame
            Dataframe cotaining all results for a certain feature/metric
        exp : str
            Experiment name
        metric : str
            Metric/feature name
        out : str
            Path to store outputs and where assemblies are stored
        samples : list
            list with sample names
        var : str
            The experiment variable
        run : str
            Run name or number, in case more than one 
        """
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out + exp + '.log',level=logging.DEBUG)
        self.df=data.copy()
        self.exp=exp
        self.metric=metric
        self.out=out
        self.samples=samples
        self.var=var
        self.run=run
        try:
            self.results=open(out+"final_stats_"+metric+run+".txt","a")
            #self.results.write(exp+" Statistics "+metric+":\n")
            print(exp+" Statistics "+metric+":\n")            

        except IOError:
            print(IOError)
            logging.error(IOError)
            
    def mean(self):
        self.results.write("\nMean:\n"+self.df.mean().to_string()+"\n")
        print("\nMean:\n"+self.df.mean().to_string()+"\n")
        self.results.write(self.df.T.mean().to_string()+"\n")
        print(self.df.T.mean().to_string()+"\n")
    
    def median(self):
         self.results.write("\nMedian:\n"+self.df.median().to_string()+"\n")
         print("\nMedian:\n"+self.df.median().to_string()+"\n")
         self.results.write(self.df.T.median().to_string()+"\n")
         print(self.df.T.median().to_string()+"\n")
    
    def standard_deviation(self):
        self.results.write("\nStandard deviation:\n"+self.df.std().to_string()+"\n")
        print("\nStandard deviation:\n"+self.df.std().to_string()+"\n")
        self.results.write(self.df.T.std().to_string()+"\n")
        print(self.df.T.std().to_string()+"\n")
        
    def scatter_plot(self,colors=[]):
        """
        Parameters
        ----------
        colors : list
            list of RGB colors to scatter plot
        """
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
        fig.savefig(self.out+self.metric+self.run+'.png', dpi=300)
        fig.clear()
        
    def normality(self):
        self.results.write("\nNormality test (shapiro)\n")
        print("\nNormality test (shapiro)\n")
        norm_col=True
        for col in self.df.columns:
            x=stats.shapiro(self.df[col]) #if normal
            self.results.write(col+" "+str(x)+"\n")
            print(col+" "+str(x)+"\n")
            if x[1]<0.05:
                norm_col=False
        norm_index=True
        for col in self.df.index:
            x=stats.shapiro(self.df.T[col]) #if normal
            self.results.write(col+" "+str(x)+"\n")
            print(col+" "+str(x)+"\n")
            if x[1]<0.05:
                norm_index=False
        return(norm_col,norm_index)
    
       
            
    def test_hypothesis(self,test):
        """
        Parameters
        ----------
        test : str
            test name 
        """
        
        module = importlib.import_module('statistical_tests.'+test.lower())
        my_class = getattr(module, test.capitalize())
        test_results=my_class(self.df,self.results)
        test_results.out=self.out
        test_results.metric=self.metric
        test_results.var=self.var
        test_results.samples=self.samples
        test_results.run=self.run
        return test_results.calculate_test()
        
    def graph(self,graph_type):
        """
        Parameters
        ----------
        graph_type : str
            graph type name
        """
        module = importlib.import_module('statistical_tests.'+graph_type.lower())
        my_class = getattr(module, graph_type.capitalize())
        test_results=my_class(self.df,self.results)
        test_results=my_class(self.df,self.results)
        test_results.out=self.out
        test_results.metric=self.metric
        test_results.var=self.var
        test_results.samples=self.samples
        test_results.run=self.run
        return test_results.calculate_test()
    
    def __table_docx(document,df):
        t = document.add_table(df.shape[0]+1, df.shape[1]+1,style='Light Grid Accent 1')
        for j in range(df.shape[-1]):
            t.cell(0,j+1).text = df.columns[j]
        for i in range (len(df.index)):
            t.cell(i+1,0).text=df.index[i]
        # add the rest of the data frame
        for i in range(df.shape[0]):
            for j in range(df.shape[-1]):
                t.cell(i+1,j+1).text = str(df.values[i,j])
                
    
    def create_report(self):
        pass
        #need to be created based on pos_analysis.py
    
class Statistics_Calculator(ABC):
    """
    Class responsable for calculating statistical tests
    
    Attributes
    ----------
    data : DataFrame
        Dataframe cotaining all results for a certain feature/metric
    results : file
        A file to save results
    metric : str
        Metric/feature name
    out : str
        Path to store outputs and where assemblies are stored
    samples : list
        list with sample names
    var : str
        The experiment variable
    run : str
        Run name or number, in case more than one 
        
    Methods
    -------
    calculate_test()
        Calculates the test
    """
    
    out='.'
    metric=''
    var=''
    samples=[]
    run=''   
 
    def __init__(self,df,arq):
        self.data=df.copy()
        self.results=arq
        super(Statistics_Calculator,self).__init__()
    @abstractmethod     
    def calculate_test(self):
        pass
        
        
        
        