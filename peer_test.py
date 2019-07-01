from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from generate_random_id import generate_id
import json
import sys
import hashlib
from datetime import datetime
from Crypto.Cipher import DES
import uuid 
import sqlite3

leafHash = []
port_number=0
choice='a'
list_id_for_peers=[]

if "pytest" not in sys.modules:
	port_number = int(sys.argv[1])
	choice=sys.argv[2]

	list_id_for_peers=sys.argv[3:]
else :
	list_id_for_peers=['abc','def']
	

class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(('localhost', port_number),requestHandler=RequestHandler)
server.register_introspection_functions()


class Test:
	def test_start(self):
		with sqlite3.connect('participants_db.db') as conn :
			cur=conn.cursor()
			cur.execute("UPDATE PARTICIPANT_BALANCE SET BALANCE=1000")
		
	def test_doubleSha256(self):
		assert(len(doubleSha256("ABC")))==64
	def test_findMerkleRoot(self):
		a=doubleSha256("ABC")
		assert(len(findMerkleRoot(a)[0]))==64
	def test_authenticate(self):
		assert(authenticate('pqr'))==0
	def test_select_table(self):
		assert(select_table())==7
	def test_read_db(self):
		assert(read_db('a')) == 1000
	def test_update_db(self):
		assert(update_db(10000,'b')) == 10000
	def test_build_tree(self):
		assert(len(build_tree()))==6
	def test_create_list_of_hashes(self):
		assert(len(create_list_of_hashes(['a','b','c','d','e','f'])))==6

a=Test()

def doubleSha256(input):
	#a=input.encode('utf-8')
	json_input=json.dumps(input)
	json_input2=json_input.encode('utf-8')
	return hashlib.sha256(json_input2).hexdigest() 
server.register_function(doubleSha256, 'doubleSha256')
	

    
def findMerkleRoot(leafHash):
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
		return findMerkleRoot(hash2)  
server.register_function(findMerkleRoot,'root')


class MyFuncs:
	def mul(self, x, y):
		return x * y
server.register_instance(MyFuncs())
	
#server.register_function(encode_id_for_peer,'encode')

def authenticate(encoded_id):
	#des = DES.new('01234567', DES.MODE_ECB)
	#print("about to decrypt")
	plain_text=encoded_id
	if(plain_text not in list_id_for_peers):
		print("client not authenticated")
		return 0
	return 1	
server.register_function(authenticate,'authenticate')
	
def select_table():
	with sqlite3.connect('participants_db.db') as conn :
		cur=conn.cursor()
		c=cur.execute("SELECT * FROM PARTICIPANT_BALANCE")
		data=len(c.fetchall())
	return data
			
server.register_function(select_table,'select_table')

def read_db(p):
	COLUMN='BALANCE'
	COLUMN2='NAME'
	
	with sqlite3.connect('participants_db.db') as conn :
		cur=conn.cursor()
		
		c=cur.execute("SELECT "+COLUMN+" FROM PARTICIPANT_BALANCE where "+COLUMN2+"=?", (p,))
		data=c.fetchone()
	return int(data[0])
server.register_function(read_db,'read')
	
def update_db(bal,p):
	COLUMN='BALANCE'
	COLUMN2='NAME'
	with sqlite3.connect('participants_db.db') as conn :
		cur=conn.cursor()
		cur.execute("UPDATE PARTICIPANT_BALANCE SET BALANCE=? WHERE NAME=?", (bal,p))
		c=cur.execute("SELECT "+COLUMN+" FROM PARTICIPANT_BALANCE where "+COLUMN2+"=?", (p,))
		data=c.fetchone()
	return int(data[0])
server.register_function(update_db,'update')

def build_tree():	
	print("1st line")
	directory = "/home/brinda/College /Sem8/project/Codes/FINAL_DEMO/Code/Input"
	print("entering the build tree")
	#choice=input("choose the first peer")
	new_f_1=directory+"/"+"dict_input_" + choice + ".txt"
	print("before opening the file\n")
	with open(new_f_1) as file:
		lines = [line.strip() for line in file]
		print("file is",lines)
	total=0
	list_of_transactions=[]
	print("before for loop")
	for line in lines :
		input1=line.split()
		print("Input is:",input1)
		involved=input1[0]
		if(choice!=involved[0]):
			print("wrong file opened")
		s_bal=int(input1[1])
		p_bal=int(input1[2])
		amount =int(input1[3])
		action=input1[4] #i want to purchase
		if("purchase" in action and choice in action):
			purchaser=choice
			seller=involved[1]
			print("purchaser is",purchaser)
			print("seller is",seller)
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
				
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			total=total+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
		elif("sell" in action and choice in action):
			seller=choice
			purchaser=involved[1]
			print("seller is",seller)
			print("purchaser is",purchaser)
				
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
		elif("sell" in action and choice not in action):
			purchaser=choice
			seller=involved[1]
			print("purchaser is",purchaser)
			print("seller is",seller)
				
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			total=total+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
				
		elif("purchase" in action and choice not in action):
			seller=choice
			purchaser=involved[1]
			print("seller is",seller)
			print("purchaser is",purchaser)
				
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
			
		x=read_db(seller)
		y=read_db(purchaser)
		print("new seller balance is",x)
		print("new purchaser balance is",y)
				
		t = {}
	

			
		tid = generate_id()
		print(tid)
		pid = generate_id()
		print(pid)
		sid = generate_id()

		t['involved'] = involved
		t['transaction_id'] = tid
		t['purchaser_id'] = pid
		t['seller_id'] = sid
		t['amount'] = amount
		t['action']=action
	

		t['new_purchaser_balance'] = y
		print("new_purchaser_balance:",y)
		t['new_seller_balance'] = x
		print("new_seller_balance:",x)
		print("transaction dictionary is",t)
		print("total amount spent by"+' '+choice+' '+"is"+' '+str(total))
		now = datetime.now()

		timestamp = datetime.timestamp(now)
		#dt_object = datetime.fromtimestamp(timestamp)
		t['timestamp']=timestamp
			
		list_of_transactions.append(t)
		print("appended")
		print("list of transactions is",list_of_transactions)
	return list_of_transactions
server.register_function(build_tree,"build")

def create_list_of_hashes(l_transactions):
	for trans in l_transactions:
		("l_transactions:",l_transactions)
		leafHash.append(doubleSha256(trans))
	return leafHash
server.register_function(create_list_of_hashes,"create")

		

if "pytest" not in sys.modules:	
	server.serve_forever()

			
