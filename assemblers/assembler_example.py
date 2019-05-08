# -*- coding: utf-8 -*-
"""
Created on Wed May  1 19:02:11 2019

@author: Your Name
"""

import os
import logging 

#Name your Assembler, use the same name to the file e.g. Spades() -> spades.py
#It must be saved at assemblers/ dir
class Assembler_name:
    """ 
    An example assembler class needed in order to insert more assemblers into 
    the Framework
   
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
    
    #please, keep all the arguments in __init__ even you do not need it
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
            if not(os.path.exists(out+"assemblies/Assembler_name/")):
                os.system("mkdir "+out+"assemblies/Assembler_name/")  
            os.system("mkdir "+out+"assemblies/Assembler_name/"+sample)
        except IOError:
            logging.error(IOError)
            exit()
            
    def run():
        """
        Run the assembly.
        """
        
        
        command="call the command here"
        os.system(command)