# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 09:51:16 2019

############################################################################
# Copyright (c) 2019 Pontifical Catholic University of Rio de Janeiro      #
# All Rights Reserved                                                      #
# See file LICENSE for details.                                            #
############################################################################

“Code is more often read than written.”
— Guido Van Rossum


@author: Guilherme Neumann
"""
import os
import logging
import multiprocessing
import reads_generator as gen
import pandas as pd
import assembly
import datetime
import stats
import evaluation as ev
import random


class Management_Core:
    
    input=dict()
    config_file='config.txt'
    ''' -------------------- Auxiliar Functions -------------------------- ''' 
    #remove blanks from the beginning of strings from a dictionary
    def __clean_dict(self,dic): 
        new=dict()
        for k,v in dic.items():
            if k[0]==' ':
                k=k[1:]
            if type(v)==list:
                for i,item in enumerate(v):
                    if item[0]==' ':
                     v[i]=item[1:]
                    
            elif v[0]==' ':
                v=v[1:]
            new[k]=v
        return new
    
    def __init__(self,config_file,input):    
        self.now = datetime.datetime.now()
    
        #receive arguments from terminal:
        #-ref stands for reference genome, -config_file for the config file
        #-t for number of threads and -o or -output for output
        
            
        try:
            self.input=input
            self.config_file=config_file
            config=open(self.config_file,'r')
            # each '-->' indicates a parameter
            for line in config:
                if '-->' in line:
                    line=line.strip().split('-->')
                    line=line[1].split(':')
                    if "," in line[1]:
                        line[1]=line[1].split(",")
                    input[line[0]]=line[1]
            self.input=self.__clean_dict(input)
            path= os.getcwd()
            if("-t" in self.input):
                self.t=self.input["-t"] #number of threads
            else:
                self.t=str(multiprocessing.cpu_count()-1)
                print("Threads number "+self.t)
            if ("-o" in self.input):
                self.output=path+"/"+self.input['-o']
            elif("-output" in self.input):
                self.output=path+"/"+self.input['-output']
            else:
                os.system("mkdir "+self.input['Experiment name'])
                self.output=path+'/'+self.input['Experiment name']+"/"
                
            if self.output[-1]!="/":
                self.output+="/"
                
            logging.basicConfig(format='%(asctime)s %(message)s', filename= self.output +self.input['Experiment name'] + '.log',level=logging.DEBUG)
            logging.info(" Beta Version (2019) - Genome Assembly Analysis Framework: ")
            variables = {'Reads len': '(2x)Reads len (bp)', 'Coverage' : 'Coverage', 'Phred':'Phred', 'Mutation':'Mutation ratio', 'Duplication':'Gene Duplication ratio', 'Multiple Genomes':'-ref' } #possible variables to the experiments
            #the chosen variable
            self.var=variables[self.input['Variable']] 
        
        except IOError:
            logging.basicConfig(filename= str(self.now.date()) + '.log',level=logging.DEBUG)
            logging.error(IOError)
            print("Errors while reading the command parameters")
            exit()
    
    '''------------------------------------ Reads Generator -----------------------------------------------------------------------'''   
    
    def reads_generation_pirs(self):
        #all samples from the variable 
        reads=gen.Reads_generation_Control(self.input['Experiment name'],self.output)
        if self.input['Reads len variation (Y/N)']=='Y':
            variation=int(self.input['If variate, how many bases'])
        else:
            variation = 0
        if type(self.input['Coverage'])!=list:
            coverage=int(self.input['Coverage'])
        if type(self.input["(2x)Reads len (bp)"])!=list:
            read=int(self.input["(2x)Reads len (bp)"])
        if type(self.input['Phred'])!=list:
            phred=int(self.input['Phred'])
        samples=[]
        for sample in self.input[self.var]:
            samples.append(int(sample))
        if self.var=='Coverage':
            coverage=samples
        elif self.var=="(2x)Reads len (bp)":
            read=samples
        elif self.var=='Phred':
            phred=samples
        print(samples)
        reads=reads.generate("pIRS",{"coverage":coverage ,"read_len":read,"ref":self.input['-ref'],
                                        "phred":phred,"mutation_rate":0,"var":variation})
        logging.info("Reads generated")
    
        return reads
    
    '''--------------------------------------------- ASSEMBLERS ------------------------------------------------------------------'''
    def assembling(self,reads):
    
        tools=assembly.Assembling_Control(reads.files, self.output, self.input["Experiment name"], self.input["(2x)Reads len (bp)"])
        if("-k" in self.input):
            tools.k=self.input["-k"]
        if self.var=='Phred':
            tools.file_format="fastq"
        tools.run(["all"])
    
            
    '''------------------------------------------ Evaluation -------------------------------------------------------------------'''
    def evaluation(self,algo,reads):
        assemblies=[]
        for sample in reads.files:
            assemblies.append({"spades":"contigs.fasta", "abyss":sample+"-contigs.fa", "velvet":"contigs.fa", "edena" : sample+"_contigs.fasta", "ssake":sample+"_contigs.fa", "masurca":"CA/9-terminator/genome.ctg.fasta", "mira":""+self.input['Experiment name']+"_assembly/"+self.input['Experiment name']+"_d_results/"+self.input['Experiment name']+"_out.unpadded.fasta",
                     "minia":"minia.contigs.fa"})
            #for further tests, we aim to use scaffolds
            #scaffolds={"masurca":"CA/9-terminator/genome.scf.fasta","spades":"scaffolds.fasta","ssake":sample+"_scaffolds.fa"} 
        metrics=ev.Evaluation_Control(self.input['-ref'], self.input['Experiment name'],self.output)
        if self.var=="Phred":
            metrics.file_format="fastq"
        metrics.apply_features([algo],assemblies,reads.files)
        
                    
                    
    '''---------------------------------------- Database --------------------------------------------------------------'''
    #for further apps, it would be interesting persisting results in a database
    
    '''---------------------------------------- Statistics --------------------------------------------------------------'''
    
    def __busca(self,index,lista):
        for i,item in enumerate(lista):
            if index==item:
                return i
        return -1
                    
    def outputs_to_df(self,indexes,columns,directory):
        metrics={"Reference mapped (\\%)":dict(),"Reference coverage $\\geq$ 1x (\\%)":dict(),"Total length":dict(),"N50":dict(),"\\# contigs":dict(), "NA50":dict(), "Complete BUSCO (\\%)" :dict(), "NG50":dict(),"Partial BUSCO (\\%)":dict(), "Largest alignment":dict(),"\\# predicted genes (unique)":dict(), "Avg. coverage depth":dict(),
                 "\\# mismatches per 100 kbp":dict(),"Mapped (\\%)":dict(), "\# misassemblies":dict(), "L50":dict(), "N75":dict(), "GC (\\%)":dict(), "Largest contig":dict() }
        for term in columns: #variables e.g. reads len
            for k,value in metrics.items():
                lis=[]
                for i in indexes:lis.append(0)
                #initialization
                value[term]=lis[:] 
        print(metrics)
        outs=os.listdir(directory)
        print(outs)
        for each in outs:
            exists= os.path.isfile(directory+each+"/report.tex")
            if exists:
                arq=open(directory+each+"/report.tex","r")
                for line in arq:
                    line=line.strip().split("&") 
                    if line[0].strip(" ") in metrics.keys(): #if we want this metric
                        index=each.split("--")
                        if len(index)>1:
                            i=self.__busca(index[1].strip(" "),indexes)
                            if i!=-1:
                                value=line[1].strip(" ").split(" ")
                                metrics[line[0].strip(" ")][index[0].strip(" ")][i]=float(value[0])
                arq.close()
        print(metrics)
        return metrics
    
    def stats_from_features(self,directory):
        indexes=[]
        columns=[]
        outs=os.listdir(directory)
        for each in outs:
            index=each.split("--")
            if len(index)>1:
                if index[1] not in indexes and os.path.isfile(directory+each+"/report.tex") :
                    indexes.append(index[1])
                if index[0] not in columns:
                    columns.append(index[0])
        #indexes=["spades","mira","minia","velvet","edena","ssake","abyss","masurca"]
        #columns=["reads100","reads150","reads200","reads250","reads300"]
        #Here we have columns as variables and indexes as assemblers. However, it shall be transposed in the assembler class
        print(indexes)
        print(columns)
        samples=self.input[self.var]
        samples_int=[]
        if self.var=='-ref':
            samples_int=samples[:]
        else:
            for s in samples:
                samples_int.append(int(s))
        dic=self.outputs_to_df(indexes,columns,directory)
        colors={assembler:["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]),random.choice('8*hPov^<>')] for assembler in indexes} #it creates a dict with color and marker type to each assembler, in order to keep the same pattern in all graphs
        for key,dici in dic.items():
            for k,value in dici.items():
                if len(value) > 0:
                    df=pd.DataFrame.from_dict(dici)
                    df.index=indexes
                    df.sort_index(axis=1, inplace=True) 
                    df.to_csv(self.output+key+".csv")
                    print(df.T)
                    ob=stats.Statistics(df.T, self.input["Experiment name"],self.input['Variable'],key,self.output,samples_int)
                    ob.normality()
                    equal=[]
                    for item in df.values:
                        for each in item:
                            if each not in equal:
                                equal.append(each)
                
                    if len(equal)>1:        
                        ob.oneway()
                        ob.kruskal()
                        try:
                            ob.correlation_pearson()
                        except:
                            continue
                    if self.var!="-ref":
                        ob.scatter_plot(colors)
                    
                    break
           
        