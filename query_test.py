import xmlrpc.client
import sys
import itertools
import uuid 
import time
import datetime
from collections import OrderedDict 
import json
import hashlib
import sys 
from operator import itemgetter

id_client=''
arguments=[]

if "pytest" not in sys.modules:
	id_client = sys.argv[1]
	arguments=sys.argv[2:]

class Test :

	def test_find_merkel_hash(self):
		x=find_merkel_hash(['a','b','c','d','e','f'])
		assert isinstance(x, list)
	def test_doubleSha256(self):
		assert(len(doubleSha256("ABC")))==64
	
t=Test()
			


list_transactions_all=[]
list_hashes_all=[]
list_ids=[]


def iterate_list(final_lst):
	k=[]
	for i in range(len(final_list)):

		a = final_list[i]['involved']

		k.append(a)
	
	for value in k:
		k.remove(value)
		
		rev=value[::-1]
		if(rev in k):
			for d in final_list:
				if(d['involved']==rev):
					final_list.remove(d)

	print("\n\n")
	
	
	newlist = sorted(final_list, key=itemgetter('involved')) 
	print("Master List (Without Duplicates)",newlist)
	print("\n\n")
	print("Length of Master List (Without Duplicates) ",len(newlist))
	print("\n\n")
	#gen_master_hash(newlist) 
	return newlist


def gen_master_hash(final_lst):
	master_hashes=[]
	for d in final_list:
		str_d = json.dumps(d)
		print ("dictionary for this transaction" , str(d))


		hexa = hashlib.sha256(str_d.encode()) 


		h_str_d = hexa.hexdigest()
	
		print ("The hash for transaction", h_str_d)
		master_hashes.append(h_str_d)
	hash2=find_merkel_hash(master_hashes)
	print("\n\n")
	#print("master hash is",hash2)
	return master_hash


def find_merkel_hash(leafHash):
	hash = []
	hash2 = []
	if len(leafHash) % 2 != 0:                            
		leafHash.extend(leafHash[-1:])
        
	for leaf in sorted(leafHash):                        
		hash.append(leaf)
		if len(hash) % 2 == 0:                          
			hash2.append(doubleSha256(hash[0]+hash[1]))   
			hash == []                                    
	if len(hash2) == 1:                                   
		return hash2
	else:
		#print(type(find_merkel_hash(hash2)))
		return find_merkel_hash(hash2)

def doubleSha256(input):
	#a=input.encode('utf-8')
	json_input=json.dumps(input)
	json_input2=json_input.encode('utf-8')
	return hashlib.sha256(json_input2).hexdigest() 


for port in arguments:
	s = xmlrpc.client.ServerProxy('http://localhost:'+port)
	auth=s.authenticate(id_client)
	if(auth==0):
		print("authentication failed")
		break
	print("\n")
	print("AUTHENTICATION SUCCESSFUL")
	y=s.select_table()
	print("table is",y)
	
	print("before calling build\n")
	a=s.build()
	y=s.select_table()
	print("final table after updation is",y)
	print("list of transactions is",a)
	list_transactions_all.append(a)
	b=s.create(a)
	print("list of hashes is",b)
	list_hashes_all.append(b)
	c=s.root(b)
	print("root hash for the participant is",c)
	print("coming to s2")
	#print(s.system.listMethods())

print("GLOBAL LIST OF TRANSACTIONS IS",list_transactions_all)
print("\n")
final_list = list(itertools.chain(*list_transactions_all))
print("THE LIST IS (DUPLICATES)",final_list)
print("Length of Final List (WITH DUPLICATES) is",len(final_list))
iterate_list(final_list) 
