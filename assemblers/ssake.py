# -*- coding: utf-8 -*-
"""
Created on Sun May  5 15:30:45 2019

@author: Guilherme Neumann
"""

import os
import logging 
from assembly import Assembler

class Ssake(Assembler):
    """ 
    Ssake assembler
    
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
    
    __assembler_name='ssake'
    require_fastq=False
    python_threads=True
    
            
    def run_assembly(self):
        """
        Run the assembly. It firstly runs TQSfast and/or 
        makePairedOutput2UNEQUALfiles and then ssake. By the moment, it only 
        works with Illumina.
        """
        if not(os.path.exists(self.out+"assemblies/"+self.__assembler_name)):
            os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name)  
        os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name+"/"+self.sample)        
                
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
