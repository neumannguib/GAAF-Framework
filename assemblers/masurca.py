# -*- coding: utf-8 -*-
"""
Created on Sun May  5 18:45:48 2019

@author: Guilherme Neumann
"""

import os
import logging 
from assembly import Assembler


class Masurca(Assembler):
    """ 
    Masurca assembler. Only works with fastq files.
    
    Attributes
    ----------
    __assembler_name : str
        The name of the assembler tool
        
    Methods
    -------
    run()
        Run the assembly    
    """
    
    __assembler_name='masurca'
    require_fastq=True
    python_threads=False
    
    
            
    def run(self):
        """
        Run the assembly. It uses a config file to run the assembly. 
        By the moment, it only works with Illumina.
        """
                
        try:
            if not(os.path.exists(self.out+"assemblies/masurca/"+self.sample)):
                os.system("mkdir "+self.out+"assemblies/masurca/"+self.sample)
         
            config=open(self.out+"assemblies/masurca/"+self.sample+"/config.txt","w")
            config.write("DATA \nPE= pe "+str(self.read_len*2)+" 1 "+self.out+"reads/"+self.sample+"_1."+self.file_format+" "+self.out+"reads/"+self.sample+"_2."+self.file_format+"\n")
            config.write("END \nPARAMETERS \nGRAPH_KMER_SIZE = "+str(self.k))
            config.write("\nGRID_ENGINE=SGE \nGRID_QUEUE=all.q \nCA_PARAMETERS =  cgwErrorRate=0.25 \nCLOSE_GAPS=1 \nNUM_THREADS ="+str(self.t))
            config.write("\nJF_SIZE = 20000000 \nSOAP_ASSEMBLY=0 \nEND")
            config.close()
            command = "cd assemblers/masurca/bin/; ./masurca "+self.out+"assemblies/masurca/"+self.sample+"/config.txt -o "+self.out+"assemblies/masurca/"+self.sample+"/assemble.sh | tee -a " +self.out + self.exp+ ".log"
            os.system(command)
            os.system("cd "+self.out+"assemblies/masurca/"+self.sample+"/; ./assemble.sh | tee -a " +self.out + self.exp+ ".log")           
        except IOError:
            logging.error(IOError)
            exit()
