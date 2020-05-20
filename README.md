Abstract: We propose a new Block-net approach where there is hierarchy of ledgers which gets represented finally as a network.
 Each transaction gets stored only in two places (purchaser and seller ledger) and then synced to network. The idea is to avoid mining and coming up with a better approach.
 The ledger itself is stored as a Merkle Tree. 

Steps to run the code

-Make sure that you have Python 3 installed.
-Install the following modules using the command pip3 install module_name:
1. XMLRPC
2. Json
3. Sys
4. Hashlib
5. Datetime
6. UUID
7. SQLite3 database
8. Pytest for unit testing

- We can display the transactions of 3 participants as of now on three different terminals and 
then query all on the fourth terminal.(We have 3 input files)

- First run the file sql_functions.py. This creates the database and inserts entries for participants balance.

The port numbers and IDs for authentication are passed as command line arguments.
-Open one terminal and enter:
python3 peer.py 8000 a abcdefgh lmnopqrs xyzhlmno
-Open the second terminal and enter:
python3 peer.py 8001 b abcdefgh lmnopqrs xyzhlmno
-On the third terminal enter :
python3 peer.py 8002 c abcdefgh lmnopqrs xyzhlmno
-On the fourth terminal, to query all participants' transactions, enter :
python3 query.py abcdefgh 8000 8001 8002

This gives a global list of all transactions of all participants on the fourth terminal
We also see the changes reflected in the balance of the participants in the database.

For testing :

1. For peer_test.py
Open a terminal and type : pytest -x peer_test.py

2. For query_test.py
Open a terminal and type : pytest -x query_test.py

These give a message that the test cases have passed.
