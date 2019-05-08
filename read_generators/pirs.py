# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 09:17:54 2019

@author: Guilherme Neumann
"""
import os
import logging
import threading as thr
from Bio import SeqIO
import time
import multiprocessing

class Pirs:
    """Class responsable for calling pIRS and generating its reads
    
    Attributes
    ----------
    parameters : dict
        A dictionary containing all the generation parameters
    file : list
        The list of the samples generated
        
    Methods
    -------
    fasta2fastq(file,ql,name='')
        Converts a fasta file to a fastq file
    command(sample)
        Run the Pirs command to the sample
    """
    
    t=multiprocessing.cpu_count()-2
    parameters=dict()
    files=[]
    
    
    def __init__(self, exp,out):
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
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
        logging.info(" Calling pirs tool")
        
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
                    
    def command(self,sample):
        """
        Run the pIRS command.
        
        Parameters
        ----------
        sample : str
            The sample name. It names the read files.
        """
        
        if "." in sample:
            p=sample.find(".")
            sample=sample[0:p]
        
        if self.parameters['ref'] == '':
            logging.error('There`s no reference file attached')
            exit()
        try:
            if not (os.path.exists(self.out+"reads")):
                os.system("mkdir "+self.out+"reads")
            exists1 = os.path.isfile(self.out+"reads/phred_base_1.fa")
            exists2 = os.path.isfile(self.out+"reads/phred_base_2.fa")
            #In pIRS one can not specify a unique phred value. For that reason,
            #here we convert it.
            if "phred" in sample:
                if not exists1 or not exists2:
                    command = "pirs simulate -x " + str(self.parameters['coverage']) + " -l " + str(self.parameters['read_len']) + " -v " +str(self.parameters['var'])+" -m " + str(self.parameters['read_len']*2) + " --no-indels --no-subst-errors --fasta -e 0 --no-gc-bias -o "+self.out+"reads -t "+str(self.t)+" -s phred_base "+self.parameters['ref'] + " | tee -a " +self.out+self.exp+ ".log"
                    os.system(command)
                thr1=thr.Thread(target=self.fasta2fastq,args=(self.out+"reads/phred_base_1.fa",self.parameters['phred'],self.out+"reads/"+sample+"_1"))
                thr2=thr.Thread(target=self.fasta2fastq,args=(self.out+"reads/phred_base_2.fa",self.parameters['phred'],self.out+"reads/"+sample+"_2"))
                thr1.daemon=True
                thr1.start()
                thr2.daemon=True
                thr2.start()
                while(thr1.is_alive() or thr2.is_alive()):
                    time.sleep(.10)
                        
            else:
                command = "pirs simulate -x " + str(self.parameters['coverage']) + " -l " + str(self.parameters['read_len']) + " -v " +str(self.parameters['var'])+" -m " + str(self.parameters['read_len']*2) + " --no-indels --no-subst-errors --fasta -e 0 --no-gc-bias -o "+self.out+"reads -t "+str(self.t)+" -s "+sample + " "+self.parameters['ref'] + " | tee -a " +self.out+self.exp+ ".log"
                os.system(command)
            self.files.append(sample)

        except IOError:
            logging.error(IOError)

            