# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 13:54:36 2019

@author: Guilherme Neumann
"""

import os
import logging 

class Kmergenie:
    
    def __init__(self, exp, out,sample,file_format="fa"):
        logging.basicConfig(filename= out+ exp + '.log',level=logging.DEBUG)
        try:
            if not (os.path.exists(out+"assemblies/kmer/"+sample)):
                os.system("mkdir "+out+"assemblies/kmer/"+sample)
            command = "kmergenie "+out+"reads/"+sample+"_1."+file_format+" -o "+out+"assemblies/kmer/"+sample+" | tee -a " + out+ exp+ ".log"
            os.system(command)
            self.exp=exp
            self.out=out
            
        except IOError:
            logging.error(IOError)
            
    def get_bestk(self):
        try:
            content_variable = open ( self.out+self.exp+ ".log" , "r" ) 
            file_lines = content_variable.readlines() 
            content_variable.close()
            last_line = file_lines[-4] 
            last_line=last_line.strip().split(':')
            return last_line[1][1:]
        except IOError:
            logging.error(IOError)