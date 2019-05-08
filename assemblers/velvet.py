# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:19:45 2019

@author: Guilherme Neumann
"""

import os
import logging 


class Velvet:
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
            if not(os.path.exists(out+"assemblies/velvet/")):
                os.system("mkdir "+out+"assemblies/velvet/")  
            os.system("mkdir "+out+"assemblies/velvet/"+sample)
        except IOError:
            logging.error(IOError)
            exit()
            
    def run(self):
        """
        Run the assembly. It firstly runs velveth and then velvetg. By the moment,
        it only works with Illumina.
        """
                
        try:
            command = "./assemblers/velvet/velveth "+self.out+"assemblies/velvet/"+self.sample+" "+self.k+" -shortPaired -"+self.tipo+" -separate "+self.out+"reads/"+self.sample+"_1."+self.file_format+" "+self.out+"reads/"+self.sample+"_2."+self.file_format+" | tee -a " +self.out + self.exp+ ".log"
            os.system(command)            
        except IOError:
            logging.error(IOError)
            exit()
        try:
            command_g="./assemblers/velvet/velvetg "+self.out+"assemblies/velvet/"+self.sample+" -ins_length "+str(self.read_len*2)+" -exp_cov auto"
            os.system(command_g)
        except IOError:
            logging.error(IOError)
            exit()