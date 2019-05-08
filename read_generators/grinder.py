# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 09:17:54 2019

@author: Guilherme Neumann
"""
import os
import logging

class Grinder:
    """Class responsable for calling grinder and generating its reads"""
    coverage = '200'
    read_len = '100'
    ql = ('40','20')
    var='0'
    files=[]
    python_threads=True
    
    def __init__(self, path, reference, exp,out):
        self.path= path
        self.exp=exp
        self.out=out
        logging.basicConfig(format='%(asctime)s %(message)s',filename= out+ exp + '.log',level=logging.DEBUG)
        logging.info(" Calling Grinder tool")
        if reference == '':
            logging.error('There`s no reference file attached')
            exit()
        self.ref = reference
        
    
    def command(self,sample):  
        try:
            if not (os.path.exists(self.path+"/../"+self.out+"reads")):
                os.system("mkdir "+self.path+"/../"+self.out+"reads")
            command = "grinder -rf " + self.ref + " -cf " + self.coverage + " -rd " + self.read_len + " normal " +self.var+" -ql " + self.ql[0] + " " + self.ql[1] + " -fq 1 -insert_dist " + str(self.read_len*2) + " -od "+self.out+"reads -bn "+sample+" | tee -a " + self.out+self.exp+ ".log"
            os.system(command)
            self.files.append(sample)
            os.wait()
            return True
        except IOError:
            logging.error(IOError)
            return False
            