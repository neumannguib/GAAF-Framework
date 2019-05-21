# -*- coding: utf-8 -*-
"""
Created on Sun May  5 19:29:00 2019

@author: Guilherme Neumann
"""

import os
import logging 
from assembly import Assembler

class Spades(Assembler):
    """ 
    SPAdes assembler
    
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
    run()
        Run the assembly    
    """
    
    __assembler_name='spades'
    require_fastq=False
    python_threads=False
    
    
    def run(self):
        """
        Run the assembly. By the moment, it only works with Illumina.
        """
        if not(os.path.exists(self.out+"assemblies/"+self.__assembler_name)):
            os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name)  
        os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name+"/"+self.sample)        
                
        try:
            command = "python3 assemblers/spades/bin/spades.py -k "+str(self.k)+" -1 "+self.out+"reads/"+self.sample+"_1."+self.file_format+" -2 "+self.out+"reads/"+self.sample+"_2."+self.file_format+" --only-assembler -o "+self.out+"assemblies/spades/"+self.sample+" | tee -a " +self.out + self.exp+ ".log"
            os.system(command)            
        except IOError:
            logging.error(IOError)
            exit()
       