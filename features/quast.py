# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 12:55:03 2019

@author: Guilherme Neumann
"""

import os
import logging

class Quast:
    """Quast tool for Genome Assembly Evaluation Metrics generation
    
    Attributes
    ----------
    file_format : str
            the format of the reads, generally fa or fq 
            
    Methods
    -------
    command(sample,t, assembler)
        Runs quast command
    """
   
    file_format="fa"
    
    
    def __init__(self, path, reference, exp,out):
        """
        Parameters
        ----------
        path : str
            Path to the assembly
        reference : str
            Genome Reference
        exp : str
            The Experiment Name
        out : str
            The output directory to store the results and where the reads 
            are stored
        """
        
        self.path=path
        self.exp=exp
        self.out=out
        if not (os.path.exists(self.out+"features/quast/")):
            os.system("mkdir "+self.out+"features/quast/")
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
        logging.info(" Calling Quast tool")
        if reference == '':
            logging.error('There`s no reference file attached')
            exit()
        self.ref = reference
        
    
    def command(self,sample,t, assembler): 
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
            command = "python3 quast/quast.py -r "+self.ref+" -t "+str(t)+" -o " + self.out+ "features/quast/"+sample+"--"+assembler+" --glimmer --rna-finding -b -1 "+self.out+"reads/"+sample+"_1."+self.file_format+" -2 "+self.out+"reads/"+sample+"_2."+self.file_format+" "+self.path+" | tee -a " + self.out+self.exp+ ".log"
            os.system(command)

        except IOError:
            logging.error(IOError)
