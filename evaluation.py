# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:58:00 2019
@author: Guilherme Neumann
"""

import os
import logging
import importlib
import multiprocessing
from abc import ABC, abstractmethod

class Evaluation_Controller:
    """Genome Evaluation Step
    
    Attributes
    ----------
    file_format : str
            the format of the reads, generally fa or fq 
    read_files : list
        List to the files containing the sequencing reads
    reference : str
        Genome reference path
    assemblies : list
        List to assembly files
            
    Methods
    -------
    apply_features(self, tools, assemblies, reads )
        Generate the features
    """
   
    file_format="fa"
    read_files=[]
    reference=''
    assemblies=[]
    
    
    def __init__(self, reference, exp,out):
        """
        Parameters
        ----------
        reference : str
            Reference Genome
        exp : str
            The Experiment Name
        out : str
            The output directory to store the results and where the reads 
            and assemblies are stored
        """
        
        
        self.exp=exp
        self.out=out
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
        logging.info(" Calling Evaluation tools")
        if reference == '':
            logging.error('There`s no reference file attached')
            exit()
        self.ref = reference
        if not (os.path.exists(self.out+"features")):
            os.system("mkdir "+self.out+"features")
    
    def apply_features(self, tools, assemblies, reads ):
        """
        Generates the features
        
        Parameters
        ----------
        tools : list
            List of tools, such as quast, to generate features. These tools must
            be stored in features/ dir.
        assemblies : list
            List of dictionaries informing for each assembler, where to find the
            final assembly, as contigs, or scaffolds. e. g.
            assemblies=[{"spades":"contigs.fasta", "abyss":reads100-contigs.fa"}, 
            {"spades":"contigs.fasta", "abyss":reads150-contigs.fa"}]
            EACH ASSEMBLY IS STORED INSIDE A DIR NAMED AS THE ASSEMBLER NAME
            it measn for reads100 sample, it has a assembly spades/contigs.fasta
            and abyss/reads100-contigs.fa.
        reads : list
            A list of the raw reads names (does not include format), ordered according 
            to assemblies
        """
        
        for tool in tools: 
        
            module = importlib.import_module('features.'+tool.lower())
            my_class = getattr(module, tool.capitalize() )
            if not (os.path.exists(self.out+"features/"+tool.lower())):
                os.system("mkdir "+self.out+"features/"+tool.lower())
            t=multiprocessing.cpu_count()-1
            for j,sample in enumerate(reads):
                logging.info(" Sample:"+sample)
                print("\n======================Sample:"+sample+"=================================================")
                logging.info("======================Sample "+sample+"=================================================")
                
                for k,v in assemblies[j].items(): 
                    try:
                        logging.info(" Evaluation:")
                        print("Evaluation:")
                        if type(self.ref)==list:
                            ref=self.ref[j]
                        else:
                            ref=self.ref
                        exists = os.path.isfile(self.out+"assemblies/"+k+"/"+sample+"/"+v)
                        if exists:
                            software=my_class(self.out+"assemblies/"+k+"/"+sample+"/"+v,ref, self.exp,self.out)
                            software.reads_format=self.file_format
                            software.calculate(sample,t,k)
                    except TypeError:
                        logging.error(TypeError) 
                        exit()

class Feature_Calculator(ABC):
    """Feature for Genome Assembly Evaluation 
    
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
    calculate(sample,t, assembler)
        Runs quast command
    """
    
    reads_format="fa"
    reference=''
    assembly=''
    
    
    def __init__(self, assembly, reference, exp,out):
        """
        Parameters
        ----------
        assembly : str
            Path to the assembly
        reference : str
            Genome Reference
        exp : str
            The Experiment Name
        out : str
            The output directory to store the results and where the reads 
            are stored
        """
        
        self.assembly=assembly
        self.exp=exp
        self.out=out
        super(Feature_Calculator,self).__init__()
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
        if reference == '':
            logging.error('There`s no reference file attached')
            exit()
        self.ref = reference
        
    @abstractmethod
    def calculate(self,sample,t, assembler): 
        """
        It calculates the feature, and outputs a report.tex.
        
        Parameters
        ----------
        sample : str
            Sample name
        t : int
            Number of threads
        assembler : str
            Assembler name
        """
        
        pass
    
