# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 14:22:39 2019

@author: Guilherme Neumann
"""
import os
import logging
from Bio import SeqIO
from read_generators import grinder
from read_generators import pirs
from features import quast
import kmergenie as kmer
from assemblers import spades as sp
from assemblers import abyss as ab
from assemblers import velvet as vb
from assemblers import edena as ed
from assemblers import ssake as ss
from assemblers import masurca as ma
from assemblers import mira as mi
from assemblers import minia
from assemblers import bcalm as bi
import reads_generator as gen
import pandas as pd
import stats

class unit_tests:
    def __init__(self):
         logging.basicConfig(format='%(asctime)s %(message)s',filename= 'tests/tests.log',level=logging.DEBUG)
         if not (os.path.exists("tests/assemblies")):
             os.system("mkdir tests/assemblies")
         
    def kmergenie(self,exp):
        try:
            logging.info(" Kmergenie:")
            k=kmer.Kmergenie(exp,"tests/","test1")
            print(k.get_bestk())
        except TypeError:
            logging.error(TypeError)
            
    def fasta2fastq(self,file,ql): 
        fq=file[0:len(file)-3] + ".fastq"
        print(fq)
        with open(file, "r") as fasta, open(fq, "w") as fastq:
            for record in SeqIO.parse(fasta, "fasta"):
                record.letter_annotations["phred_quality"] = [ql] * len(record)
                SeqIO.write(record, fastq, "fastq")
    
    def abyss(self,exp,read_len,k):
        try:
            logging.info(" Abyss:")
            genome=ab.Abyss("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/","test1",read_len,'fa',k,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
    
    def spades(self,exp, read_len,k):
        try:
            logging.info(" Spades:")
            genome=sp.Spades("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/","test1",read_len,'fa',k,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
    
    def velvet(self,exp, read_len,k):
        try:
            logging.info(" Velvet:")
            genome=vb.Velvet("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/","test1",read_len,'fa',k,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
            
    def edena(self,exp,read_len,k):
        try:
            logging.info(" Edena:")
            genome=ed.Edena("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/","test1",read_len,'fa',k,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
            
    def ssake(self,exp, read_len):
        try:
            logging.info(" Ssake:")
            genome=ss.Ssake("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/",'test1',read_len,'fa',None,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
            
    def masurca(self,exp,read_len,k):
        try:
            os.system("mkdir tests/assemblies/masurca")
            logging.info(" Masurca:")
            genome=ma.Masurca("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/","phred_test",read_len,"fastq",k,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
            
    def mira(self,exp,read_len,k):
        try:
            os.system("mkdir tests/assemblies/mira")
            logging.info(" Mira:")
            genome=mi.Mira("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/","phred_test",read_len,"fastq",k,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
    
    def minia(self,exp,read_len,k):
        try:
            os.system("mkdir tests/assemblies/minia")
            logging.info(" Minia:")
            genome=minia.Minia("Illumina",exp,"/home/gneumann/gaaf/unit_tests/tests/","test1",read_len,"fa",k,16)
            genome.run()
        except TypeError:
            logging.error(TypeError)
            
    def bcalm(self,exp):
        try:
            os.system("mkdir tests/assemblies/bcalm")
            logging.info(" Bcalm:")
            bi.Bcalm(exp,"tests/","reads100",'31','14')
        except TypeError:
            logging.error(TypeError)
            
    def Grinder(path, reference, exp):
        try:
            logging.info(" Grinder:")
            reads = grinder.Grinder(path,reference, exp,"/home/gneumann/gaaf/unit_tests/tests/")
            reads.coverage = '200'
            reads.ql = '40'
            reads.var='0'
            reads.command('test1')
            logging.info(" Reads generated")
        except TypeError:
            logging.error(TypeError)

    def Pirs(self, exp, out):
        try:
            logging.info(" Pirs:")
            reads = pirs.Pirs(exp,out)
            reads.parameters={"coverage":30,"read_len":100,"ref":"teste.fasta",
                              "phred":40,"mutation_rate":0,"var":0}
            reads.command('test1')
            reads.command('phred_test')
            logging.info("Reads generated")
        except TypeError:
            logging.error(TypeError)
            
    def Reads_Generator(self, exp, out):
        try:
            logging.info(" Reads_Generator:")
            reads=gen.Reads_generation_Control(exp,out)
            reads.generate("pIRS",{"coverage":30,"read_len":[100,150],"ref":"teste.fasta",
                                    "phred":40,"mutation_rate":0,"var":0})
            logging.info("Reads generated")
        except TypeError:
            logging.error(TypeError)
            
    def Quast(self,path, reference, exp,):
        try:
            logging.info(" Quast:")
            q=quast.Quast(path, reference, exp,"/home/gneumann/gaaf/unit_tests/tests/")
            q.run('test1',15,'spades')
            logging.info(" Metrics generated")
        except TypeError:
            logging.error(TypeError)
            
    def Statistics(self, exp):
        try:
            df={'spades': [1,2,5,6,7,6,9,8,7,5], 'abyss': [3,3,6,4,6,7,7,4,3,9],'edena': [0,32,9,6,4,4,9,8,8,7], 'ssake': [5,5,6,8,6,8,7,4,3,9]}
            df = pd.DataFrame(data=df)
            logging.info(" Stats:")
            ob=stats.Statistics(df, exp,"Reads len","N50","/home/gneumann/gaaf/unit_tests/tests/",[50,100,150,200,250,300,350,400,450,500])
            ob.normality()
            ob.oneway()
            ob.kruskal()
            ob.scatter_plot()
            ob.linear_regression_all_samples()
            
        except TypeError:
            logging.error(TypeError)
            
    def __busca(self,index,lista):
        for i,item in enumerate(lista):
            if index==item:
                return i
        return -1
            
    def outputs_to_df(self, indexes,columns):
        metrics={"N50":dict(),"\\# contigs":dict(), "NA50":dict(), "Complete BUSCO (\\%)" :dict()}
        for term in columns: #variables e.g. reads len
            for k,value in metrics.items():
                lis=[]
                for i in indexes:lis.append(0)
                value[term]=lis[:] #initialization
        print(metrics)
        outs=os.listdir("tests/quast")
        print(outs)
        for each in outs:
            exists= os.path.isfile("/home/gneumann/gaef/unit_tests/tests/quast/"+each+"/report.tex")
            if exists:
                arq=open("/home/gneumann/gaef/unit_tests/tests/quast/"+each+"/report.tex","r")
                for line in arq:
                    line=line.strip().split("&") 
                    
                    if line[0].strip(" ") in metrics.keys(): #if we want this metric
                        
                        index=each.split("_")
                        if len(index)>1:
                            i=self.__busca(index[1].strip(" "),indexes)
                            if i!=-1:
                                value=line[1].strip(" ").split(" ")
                                metrics[line[0].strip(" ")][index[0].strip(" ")][i]=float(value[0])
                arq.close()
        print(metrics)
        return metrics
    
    '''def Alf(self, out, reference, exp):
        try:
            logging.info(" Alf:")
            reads = alf_sim.ALF(exp,reference,out,"test")
            reads.duplication(0.01)
            logging.info("Duplication tested")
        except TypeError:
            logging.error(TypeError)'''
    
    