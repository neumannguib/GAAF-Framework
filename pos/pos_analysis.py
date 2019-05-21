# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 10:44:10 2019

@author: Guilherme Neumann
"""
import os
import stats
import pandas as pd
from scipy import stats as stat
import numpy as np
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt 
import random

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

def tests(data,document,met,colors,run=''):
    df=data.copy()
    t = document.add_table(df.shape[0]+1, df.shape[1]+1,style='Light Grid Accent 1')
    for j in range(df.shape[-1]):
        t.cell(0,j+1).text = df.columns[j]
    for i in range (len(df.index)):
        t.cell(i+1,0).text=df.index[i]
    # add the rest of the data frame
    for i in range(df.shape[0]):
        for j in range(df.shape[-1]):
            t.cell(i+1,j+1).text = str(df.values[i,j])
    #object stats        
    ob=stats.Statistics(df,exp,var,met,"outputs_csv/",samples_int,run)
    if var!="Ecoli strains" and not os.path.isfile(out+met+".png" and run==''):
        ob.scatter_plot(colors)
        document.add_picture(out+met+'.png', width=Inches(6.25))
    norms=ob.normality()
    equal=[]
    for item in df.values:
        for each2 in item:
            if each2 not in equal:
                equal.append(each2)
        #check if all the results are not the same. At least one need to be different    
    if len(equal)>1:
        if norms[0] and norms[1]:
            anova=ob.oneway()
            anova_assemblers=anova[0].pvalue
            anova_reads=anova[1].pvalue
            if anova_assemblers <0.05 or  anova_reads<0.05:
                pass
            #ob.tukey_test()
            #ob.bonferroni_test()
        else:
            k=ob.kruskal()
            pk_assemblers=k[0].pvalue
            pk_reads=k[1].pvalue
            if pk_assemblers <0.05 or  pk_reads<0.05:
                ob.nemenyi_test()
                ob.correlation_pearson()
                document.add_picture(out+'corr_'+met+'.png', width=Inches(7.25))
                try:
                    ob.linear_regression()                        
                except:
                    pass                    
    ob.results.close()    
            
    temp=open("outputs_csv/final_stats_"+met+""+run+".txt")
    for line in temp:
        document.add_paragraph(line.strip(), style='List Bullet')
    df.index=samples_int
    if not os.path.isfile(out+met+'_plot'+run+'.png'):
        df[var]=samples
        df.plot(x=var, title=met)
        plt.ylabel(met)
        plt.xticks(rotation=90)
            
        fig = plt.gcf()
        fig.set_size_inches(12, 8)
        fig.savefig(out+met+'_plot'+run+'.png', dpi=300)
        fig.clear()
    document.add_picture(out+met+'_plot'+run+'.png', width=Inches(7.25))
            
    if not os.path.isfile(out+met+'_box'+run+'.png'):
        df.plot.box(title=met,whis=3)
        plt.ylabel(met)
        plt.xticks(rotation=90)
        
        fig = plt.gcf()
        fig.set_size_inches(12, 8)
        fig.savefig(out+met+'_box'+run+'.png', dpi=300)
        fig.clear()
            
    document.add_picture(out+met+'_box'+run+'.png', width=Inches(7.25))
    return ob

exp=input("Experiment Name: ")
var=input("Type the variable of the Experiment: ")
samples=input("and the samples variation separated by comma (e.g. 100,150,200,250,300):")
document = Document()
document.add_heading("Complete Report "+exp, 0)

samples=samples.split(",")
samples_int=[]
for s in samples:
    samples_int.append(int(s))
metrics={}
outs=os.listdir("outputs_csv")
out="outputs_csv/"
colors=[]
for each in outs:    
    
    met=each.split(".")
    if met[1]=="csv" and "corr_" not in met[0]:
        df=pd.read_csv(out+each, header=0, index_col=0)
        
        metrics[met[0]]=df.T #for each metric in the dir, we create a dataframe
        if colors==[]:
            colors={assembler:["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]),random.choice('8*hPov^<>')] for assembler in df.index} #it creates a dict with color and marker type to each assembler, in order to keep the same pattern in all graphs

        document.add_heading(met[0], level=1)
        ob=tests(metrics[met[0]],document,met[0],colors)
        
        document.add_heading("Removing SSAKE from data:", level=2)
        metrics[met[0]]=metrics[met[0]].drop(['ssake'],axis=1)
        ob=tests(metrics[met[0]],document,met[0],colors,'without_ssake')       
        
        z=np.abs(stat.zscore(metrics[met[0]]))
        print(np.where(z>3))   
        
        if np.where(z>3)[0]!=[]:
            document.add_heading("Removing outliers through Zscore", level=2)
            metrics[met[0]]=metrics[met[0]][(z<3).all(axis=1)] 
            document.add_paragraph(str(np.where(z>3)), style='List Bullet')
            ob=tests(metrics[met[0]],document,met[0],colors,'without_zscore')                      
        
        
            
        document.save(exp+".docx")

 
        