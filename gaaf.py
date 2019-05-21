# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:28:06 2019
############################################################################
# Copyright (c) 2019 Pontifical Catholic University of Rio de Janeiro      #
# All Rights Reserved                                                      #
# See file LICENSE for details.                                            #
############################################################################

“Code is more often read than written.”
— Guido Van Rossum

@author: Guilherme Neumann
"""
import sys
import management
total = len(sys.argv)
args = sys.argv           
input=dict()
i=0
while i<total:
    if args[i][0]=='-':
        if args[i]=='-help' or args[i]=='--help' or args[i]=='-h' or args[i]=='--':
            print("############################################################################\n\
        # Copyright (c) 2019 Pontifical Catholic University of Rio de Janeiro      #\n\
        # All Rights Reserved                                                      #\n\
        # See file LICENSE for details.                                            #\n\
        ############################################################################\n\
        Beta Version (2019) - Genome Assembly Analysis Framework:\n\
        Usage: gaef.py -ref <fasta_file> -config_file <config.txt> -t <Threads_Number> -o <output_dir>\n\
        Options:\n\
        -o/-output              directory to store results\n\
        -ref                    fasta file to the reference genome (required)\n\
        -config_file            configuration file, see config.txt example (required)\n\
        -k                      k-mer length. If not informed, it's generated through kmergenie\n\
        -t                      Number of threads\n\
        -h/--help               print this usage message")
            exit()
                
        if "," in args[i+1]:
            input[args[i]] = args[i+1].split(",")
        else:
            input[args[i]] = args[i+1]
            i+=1
    i+=1

manager=management.Management_Core(input['-config_file'],input)
reads=manager.reads_generation_pirs()
manager.assembling(reads) 
manager.evaluation("quast",reads)
manager.stats_from_features(manager.output+"features/quast/")