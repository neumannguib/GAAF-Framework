# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:16:08 2019

@author: Guilherme Neumann
"""

import os
import logging 
from assembly import Assembler

class Abyss(Assembler):
    """ 
    Abyss assembler
    
    Attributes
    ----------
    __assembler_name : str
        The name of the assembler tool
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
    
    __assembler_name='abyss'
    require_fastq=False
    python_threads=False
    
            
    def run_assembly(self):
        """
        Run the assembly. By the moment, it only works with Illumina.
        """
        if not(os.path.exists(self.out+"assemblies/"+self.__assembler_name)):
            os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name)  
        os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name+"/"+self.sample)                
        try:
            os.system("cp "+self.out+"reads/"+self.sample+"_1."+self.file_format+" " +self.out+"assemblies/abyss/"+self.sample)
            os.system("cp "+self.out+"reads/"+self.sample+"_2."+self.file_format+" " +self.out+"assemblies/abyss/"+self.sample)
            command='abyss-pe k='+ str(self.k) +' name='+self.sample+' in=\''+self.sample+'_1.'+self.file_format+' '+self.sample+'_2.'+self.file_format+'\'  --directory='+self.out +'assemblies/abyss/'+self.sample+' j='+str(self.t)+' | tee -a ' +self.out + self.exp+ '.log'
            os.system(command)          
        except IOError:
            logging.error(IOError)
            exit()
      

