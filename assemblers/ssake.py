# -*- coding: utf-8 -*-
"""
Created on Sun May  5 15:30:45 2019

@author: Guilherme Neumann
"""

import os
import logging 


class Ssake:
    """ 
    Ssake assembler
    
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
    python_threads=True
    
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
            if not(os.path.exists(out+"assemblies/ssake/")):
                os.system("mkdir "+out+"assemblies/ssake/")  
            os.system("mkdir "+out+"assemblies/ssake/"+sample)
        except IOError:
            logging.error(IOError)
            exit()
            
    def run(self):
        """
        Run the assembly. It firstly runs TQSfast and/or 
        makePairedOutput2UNEQUALfiles and then ssake. By the moment, it only 
        works with Illumina.
        """
                
        try:
            if self.file_format=="fq" or self.file_format=="fastq":
                os.system("./assemblers/ssake/tools/TQSfastq.py -f "+self.out+"reads/"+self.sample+"_1."+self.file_format)
                os.system("./assemblers/ssake/tools/TQSfastq.py -f "+self.out+"reads/"+self.sample+"_2."+self.file_format)
            command = "./assemblers/ssake/tools/makePairedOutput2UNEQUALfiles.pl "+self.out+"reads/"+self.sample+"_1."+self.file_format+" "+self.out+"reads/"+self.sample+"_2."+self.file_format+" "+str(self.read_len*2)+" | tee -a " +self.out + self.exp+ "_ssake.log"
            os.system(command)
            os.system("mv paired.fa "+self.out+"assemblies/ssake/"+self.sample)
            os.system("mv unpaired.fa "+self.out+"assemblies/ssake/"+self.sample)          
        except IOError:
            logging.error(IOError)
            exit()
        try:
            path= os.getcwd()
            command_g="cd "+self.out+"assemblies/ssake/"+self.sample+";"+path+"/assemblers/ssake/SSAKE -f paired.fa -g unpaired.fa -p 1 -w 1 -b "+self.sample+" | tee -a " +self.out + self.exp+ "_ssake.log"
            os.system(command_g)
        except IOError:
            logging.error(IOError)
            exit()
