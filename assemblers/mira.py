# -*- coding: utf-8 -*-
"""
Created on Sun May  5 19:11:58 2019

@author: Guilherme Neumann
"""

import os
import logging 
from assembly import Assembler

class Mira(Assembler):
    """ 
    Mira assembler
    
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
    
    __assembler_name='mira'
    require_fastq=True
    python_threads=False
    

    def run_assembly(self):
        """
        Run the assembly. By the moment,it only works with Illumina.
        """
        if not(os.path.exists(self.out+"assemblies/"+self.__assembler_name)):
            os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name)  
        os.system("mkdir "+self.out+"assemblies/"+self.__assembler_name+"/"+self.sample)                
        try:
            if self.file_format=='fq':
                os.system("cp "+self.out+"reads/"+self.sample+"_1."+self.file_format+" "+self.out+"reads/"+self.sample+"_1.fastq")
                os.system("cp "+self.out+"reads/"+self.sample+"_2."+self.file_format+" "+self.out+"reads/"+self.sample+"_2.fastq")
                self.file_format='fastq'
            manifest=open(self.out+"assemblies/mira/"+self.sample+"/manifest.txt","w")
            manifest.write("project="+self.exp+"\njob = genome,denovo,accurate\n")
            manifest.write("readgroup = DataIlluminaPairedLib \ntechnology = solexa \ndata ="+self.out+"reads/"+self.sample+"_1."+self.file_format+" "+self.out+"reads/"+self.sample+"_2."+self.file_format+"\n")
            manifest.write("segment_placement = ---> <--- \ntemplate_size = "+str(int(self.read_len)*2)+ " "+str(int(self.read_len)*2)+" autorefine")
            manifest.close()
            command = "./assemblers/mira/bin/mira "+self.out+"assemblies/mira/"+self.sample+"/manifest.txt -t "+str(self.t)+" -c "+self.out+"assemblies/mira/"+self.sample+" | tee -a " +self.out + self.exp+ ".log"
            os.system(command)           
        except IOError:
            logging.error(IOError)
            exit()
       