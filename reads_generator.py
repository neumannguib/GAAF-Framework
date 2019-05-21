# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 09:44:03 2019

@author: Guilherme Neumann
"""

from Bio import SeqIO
import logging
import importlib
import threading as thr
import multiprocessing
import time
import os
from abc import ABC, abstractmethod

class Reads_generation_Control():
    """
    This Class generates artifitial sequencing reads through third-party 
    algorithms. Not only one can generate reads for a unique assemblies,
    but also multiple read datasets, for multiple assemblies, varying 
    parameters. For that, just provide a list o values for the selected 
    parameter.
    
    Methods
    -------
    fasta2fastq(file,ql,name='')
        Converts a fasta file to a fastq file
    generate(alg,parameters)
        The method where the reads are generated
    """

    
    def __init__(self, exp, out ):
        """
        Parameters
        ----------
        exp : str
            The Experiment Name
        out : str
            The output directory to store the results and where the reads 
            are stored
        """
        self.exp=exp
        self.output=out
        
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
        
                    
    def generate(self,alg,parameters):
        """
        Here the reads are generated.
        
        Parameters
        ----------
        alg : str
            The selected algorithm. Please be sure the alg.py is provided on
            read_generators/.
        parameters : dict
            A dictionary containing all the generation parameters. Be sure of
            providing the same syntax for the keys from the selected algorithm.
            
        Returns
        -------
        reads object
            an object instance of the algorithm. It is worth for getting 
            parameters and sample names later.
        """
        
        if not (os.path.exists(self.output+"reads")):
            os.system("mkdir "+self.output+"reads")
        module = importlib.import_module('read_generators.'+alg.lower())
        my_class = getattr(module, alg.capitalize() )
        reads = my_class(self.exp ,self.output)
        t=multiprocessing.cpu_count()-1
        samples=[]
        for par,value in parameters.items():
            if type(value) !=list:
                reads.parameters[par]=value
            else:
                samples=value
                var=par
        threads=[]
        exists = os.path.isfile(self.output+"reads/run_generator.log")
        done=[]
        if exists:
            last_run=open(self.output+"reads/run_generator.log","r")
            done=last_run.read().split("\n")
        run_log=open(self.output+"reads/run_generator.log","a")
        if samples!=[]:
            reads.t=t//len(samples)
            if reads.t<0:
                reads.t=1
            for sample in samples:
                reads.parameters[var]=sample
                sample=var+"_"+ str(sample)
                if sample not in done:
                    threads.append(thr.Thread(target=reads.command,args=(sample,)))
                    threads[-1].daemon=True
                    threads[-1].setName(sample)
                    threads[-1].start()
                else:
                    reads.files.append(sample)
        elif self.exp not in done:
            reads.t=t
            threads.append(thr.Thread(target=reads.command,args=(self.exp,)))
            threads[-1].daemon=True
            threads[-1].setName(self.exp)
            threads[-1].start()
                                                   
        for thread in threads:        
            while(thread.is_alive()):
                time.sleep(.10)
            else:
                run_log.write(thread.getName()+"\n")
               
        run_log.close()        
        print(" Reads generated")
        logging.info("Reads generated")
        
        
        return reads

class Generator(ABC):
    """
    Abstract class responsable for generating reads
    
    Attributes
    ----------
    parameters : dict
        A dictionary containing all the generation parameters
    files : list
        The list of the samples generated
        
    Methods
    -------
    fasta2fastq(file,ql,name='')
        Converts a fasta file to a fastq file
    command(sample)
        Run the command to the sample
    """
    
    t=multiprocessing.cpu_count()-2
    parameters=dict()
    files=[]
    
    def __init__(self,exp,out):
        """
        Parameters
        ----------
        exp : str
            The Experiment Name
        out : str
            The output directory to store the results and where the reads 
            are stored
        """
        
        self.exp=exp
        self.out=out
        super(Generator,self).__init__()
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
    
    
    def fasta2fastq(self,file,ql,name=''): 
        """
        It converts a fasta file to a fastq file.
        
        Parameters
        ----------
        file : str
            file name, including format, e.g. 'reads_1.fa'
        ql : int
            phred number
        """
        
        
        try:
            if name!='':
                fq=name+".fastq"
            else:
                fq=file.split(".")
                fq=fq[0] + ".fastq"
            with open(file, "r") as fasta, open(fq, "w") as fastq:
                for record in SeqIO.parse(fasta, "fasta"):
                    record.letter_annotations["phred_quality"] = [ql] * len(record)
                    SeqIO.write(record, fastq, "fastq")
            fasta.close()
            fastq.close()
        
        except IOError:
                    logging.error(IOError)
                    exit()
                  
                    
    @abstractmethod
    def command(self,sample):
        """
        Run the command.
        """
        pass
    

