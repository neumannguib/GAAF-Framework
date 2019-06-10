# -*- coding: utf-8 -*-
"""
Created on Sun May  5 18:35:56 2019

@author: Guilherme Neumann
"""

import os
import logging 
from assembly import Assembler

class Edena(Assembler):
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
    
    __assembler_name='edena'
    require_fastq=False
    python_threads=False

    def run_assembly(self):
        """
        Run the assembly. It firstly generates an ovl file, then it runs the 
        assembly. By the moment, it only works with Illumina.
        """
        if not(os.path.exists(self.out+"assemblies/"+self.__assembler_name)):
            os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name)  
        os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name+"/"+self.sample)        
                
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
