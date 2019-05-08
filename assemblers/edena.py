# -*- coding: utf-8 -*-
"""
Created on Sun May  5 18:35:56 2019

@author: Guilherme Neumann
"""

import os
import logging 


class Edena:
    """ 
    Velvet assembler
    
    Attributes
    ----------
    require_fastq : bool
        if the assembler only work with fastq files, please set as True 
        (default False)
    python_threads : bool
        in case the assembler do not use multithread, you can at least 
        activate it to run with python threads. Those threads are used 
        by Assembly Module (default False).
        
    Methods
    -------
    run()
        Run the assembly    
    """
    
    
    require_fastq=False
    python_threads=False
    
    def __init__(self, technology, exp, out, sample,read_len,file_format,k,t):
        """
        Parameters
        ----------
        technology : str
            the sequencing technology, e.g. Illumina
        exp : str
            The Experiment Name
        out : str
            The output directory to store the results and where the reads 
            are stored
        sample : str
            Sample Name (assembly name)
        read_len : int
            The average reads length 
        file_format : str
            the format of the reads, generally fa or fq 
        k : int
            the k-mer number used in k-based assemblers
        t : int
           Number of threads
        """
        
        
        self.tech=technology
        self.exp=exp
        self.out=out
        self.sample=sample
        self.read_len=read_len
        self.file_format=file_format
        self.k=k
        self.t=t
        try:
            #Using the shared logging system
            logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
            if file_format=="fa" or file_format=="fasta" or file_format=="fna":
                self.tipo="fasta"
            else:
                self.tipo="fastq"
            if not(os.path.exists(out+"assemblies/edena/")):
                os.system("mkdir "+out+"assemblies/edena/")  
            os.system("mkdir "+out+"assemblies/edena/"+sample)
        except IOError:
            logging.error(IOError)
            exit()
            
    def run(self):
        """
        Run the assembly. It firstly generates an ovl file, then it runs the 
        assembly. By the moment, it only works with Illumina.
        """
                
        try:
            command = "./assemblers/edena/bin/edena -nThreads "+str(self.t)+" -paired "+self.out+"reads/"+self.sample+"_1."+self.file_format+" "+self.out+"reads/"+self.sample+"_2."+self.file_format+" -p "+self.sample+" | tee -a " +self.out + self.exp+ ".log"
            os.system(command)          
        except IOError:
            logging.error(IOError)
            exit()
        try:
            command_g="./assemblers/edena/bin/edena -e "+self.sample+".ovl -nThreads "+str(self.t)+" -p "+self.sample+" | tee -a " +self.out + self.exp+ ".log"
            os.system(command_g)
            os.system("mv "+self.sample+"* "+self.out+"assemblies/edena/"+self.sample)
        except IOError:
            logging.error(IOError)
            exit()
