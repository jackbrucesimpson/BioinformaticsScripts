#! /usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        MassCDD
# Purpose:     Takes all the sequences in a fasta file and runs them against the NCBI Conserved Domain Database
#
# Author:      Jack Simpson
#
# Created:     05/07/2013
#-------------------------------------------------------------------------------

import sys
from Bio import SeqIO
from Bio import Seq
import time
import requests
import lxml.html
import lxml
import webbrowser

seq_list = []
fasta_file="example.fasta"
for seq_rec in SeqIO.parse(fasta_file, "fasta"):
    seq_list.append(seq_rec)

for each_seq in seq_list:
    session = requests.session()
    url = "http://www.ncbi.nlm.nih.gov/Structure/cdd/wrpsb.cgi"
    form_data = {'seqinput': each_seq.seq}
    
    try_count = 0
    while True:
        try_count += 1
    
        print 'Request....'
        r = session.post(url, form_data)
        with open('store.html'.format(try_count), 'wb') as f:
            f.write(r.content)
    
        root = lxml.html.fromstring(r.content)
    
        form_data = {input_.get('name'): input_.get('value') for input_ in root.cssselect('#_refresh input')}
        if not form_data:
            break
        form_data['tick'] = '10000'
    
        print 'Wait for 10 seconds.'
        time.sleep(10)
    
    print 'Done'
    rid = root.cssselect('#div_search_info table.searchdata tr:nth-child(1) td:nth-child(2) strong')[0].tail.strip()

    op_file = open("store.html","r")
    file_contents = file.read(op_file)
    op_file.close()
    
    root2 = lxml.html.fromstring(file_contents)
    find_cells = root2.find_class("detail backstage")
    find_more_cells = root2.find_class("detail shadowed backstage")
    
    all_cells = find_cells + find_more_cells
    
    list_all_results = []
    for i in all_cells:
        ii = lxml.html.tostring(i)
        iii = ii.split("<pre>")
        done = lxml.html.fromstring(iii[0]).text_content()
        list_all_results.append(done)
        
    print seq_list.id, "of length", len(seq_list.seq)
    print list_all_results

