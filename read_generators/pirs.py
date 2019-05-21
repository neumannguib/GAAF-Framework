# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 09:17:54 2019

@author: Guilherme Neumann
"""
import os
import logging
import threading as thr
import time
from reads_generator import Generator

class Pirs(Generator):
    """Class responsable for calling pIRS and generating its reads
    
    Attributes
    ----------
    __tool_name : str
        the algorithm name
    
    Methods
    -------
    command(sample)
        Run the Pirs command to the sample
    """
    
    tool_name='pirs'

                    
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

            