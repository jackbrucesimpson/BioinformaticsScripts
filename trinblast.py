
import re
import csv

input_blast_result_file = "/Users/u5305887/Desktop/S11.2blast.txt"
input_trinity_file = "/Users/u5305887/Desktop/TrinityS11.2.fasta"
output_csv_file = '/Users/u5305887/Desktop/S11.2.csv'

open_file = open(input_blast_result_file, "r")
read_file = open_file.read()
open_file.close()

split_queries = read_file.split("Query= ")
del split_queries[0]
found_queries = []
for each_query in split_queries:
	if "***** No hits found *****" not in each_query.lower():
		found_queries.append(each_query)

query_length = len(found_queries)
counter = 1
open_trin = open(input_trinity_file, "r")
read_trin = open_trin.read()
open_trin.close()

split_trin = read_trin.split(">")
del split_trin[0]
#print split_trin[0]

for each_split_query in found_queries:
	print counter, "of", query_length, "done"
	adding_final=[]
	split_query_id = each_split_query.split("\n")[0]
	adding_final.append(split_query_id)

	seq_len = re.search("Length=(.*?)\n",each_split_query)
	adding_final.append(seq_len.group(1))

	sig_line = re.search("Sequences producing significant alignments:                          \(Bits\)  Value\n\n(.*?)\n",each_split_query)
	sig_id = re.search("\|(.*?)\|",sig_line.group(1)).group(1)
	split_first_id = each_split_query.split(sig_id)
	sig_head = re.search("\|(.*?)Length",split_first_id[2],re.S)
	adding_final.append(sig_id + sig_head.group(1))
	#adding_final.append(sig_id + sig_head.group(1))
	if re.search("Expect = (.*?)\\n",split_first_id[2]) != None:
		expect = re.search("Expect = (.*?)\\n",split_first_id[2]).group(1)
		adding_final.append(expect)
	else:
		expect = re.search("Expect\(2\) = (.*?),",split_first_id[2]).group(1)
		adding_final.append(expect)

	for trinity_seq in split_trin:
		if split_query_id in trinity_seq.split("\n")[0]:
			query_seq = trinity_seq.split(trinity_seq.split("\n")[0])[1][1:]
			adding_final.append(query_seq)

	counter += +1		
	csv_file = open(output_csv_file, 'a')
	writing = csv.writer(csv_file)
	writing.writerow(adding_final)
