# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:19:45 2019

@author: Guilherme Neumann
"""

import os
import logging 
from assembly import Assembler

class Velvet(Assembler):
    """ 
    Velvet assembler
    
    Attributes
    ----------
    __assembler_name : str
        The name of the assembler
    require_fastq : bool
        if the assembler only work with fastq files, please set as True 
        (default False)
    python_threads : bool
        in case the assembler do not use multithread, you can at least 
        activate it to run with python threads. Those threads are used 
        by Assembly Module (default False).
        
    Methods
    -------
    run_assembly()
        Run the assembly    
    """
    
    __assembler_name='velvet'
    require_fastq=False
    python_threads=False
    
    
            
    def run_assembly(self):
        """
        Run the assembly. It firstly runs velveth and then velvetg. By the moment,
        it only works with Illumina.
        """
        if not(os.path.exists(self.out+"assemblies/"+self.__assembler_name)):
            os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name)  
        os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name+"/"+self.sample)        
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