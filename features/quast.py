# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 12:55:03 2019

@author: Guilherme Neumann
"""

import os
import logging
from evaluation import Evaluation_Tool

class Quast(Evaluation_Tool):
    """Quast tool for Genome Assembly Evaluation 
    
    Attributes
    ----------
    reads_format : str
            the format of the reads, generally fa or fq 
    reference : str
            Genome Reference
    assembly : str
            Path to the assembly
            
    Methods
    -------
    run(sample,t, assembler)
        Runs quast command
    """
    
    reads_format="fa"
    reference=''
    assembly=''
   
    
    def run(self,sample,t, assembler): 
        """
        It runs quast, and outputs report.tex.
        
        Parameters
        ----------
        sample : str
            Sample name
        t : int
            Number of threads
        assembler : str
            Assembler name
        """
        
        try:
            if not (os.path.exists(self.out+"features/quast/"+sample+"--"+assembler)):
                os.system("mkdir "+self.out+"features/quast/"+sample+"--"+assembler)
            logging.info(" Calling Quast tool")
            command = "python3 quast/quast.py -r "+self.ref+" -t "+str(t)+" -o " + self.out+ "features/quast/"+sample+"--"+assembler+" --glimmer --rna-finding -b -1 "+self.out+"reads/"+sample+"_1."+self.reads_format+" -2 "+self.out+"reads/"+sample+"_2."+self.reads_format+" "+self.assembly+" | tee -a " + self.out+self.exp+ ".log"
            os.system(command)

        except IOError:
            logging.error(IOError)
