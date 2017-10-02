#!/usr/bin/env python

import re
from io import StringIO
from Bio import SeqIO
import requests

file_name = '../finding_a_protein_motif/finding_a_protein_motif.txt'


def main():
    id_list = list(open(file_name, 'r').read().split('\n'))
    
    for id in id_list:
        request = requests.get('http://www.uniprot.org/uniprot/%s.fasta' % id).text
        
        seq = SeqIO.read(StringIO(request), 'fasta')
        motifs = [x for x in re.finditer(r'(?=(N[^P][ST][^P]))', str(seq.seq))]
        if not len(motifs):
            continue
        print(id + '\n' + ' '.join([str(motif.start(0) + 1) for motif in motifs]))


if __name__ == '__main__':
    main()

