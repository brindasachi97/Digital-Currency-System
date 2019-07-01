#This file to be run only for the first time 

import sqlite3
conn = sqlite3.connect('participants_db.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE PARTICIPANT_BALANCE 
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         BALANCE            INT     NOT NULL);''')
print("Table created successfully")
conn.close()

#Then Insert Elememnts into the database

'''insert into PARTICIPANT_BALANCE (ID, NAME, BALANCE) VALUES (1, 'a', 10000);
insert into PARTICIPANT_BALANCE (ID, NAME, BALANCE) VALUES (2, 'b', 20000);
insert into PARTICIPANT_BALANCE (ID, NAME, BALANCE) VALUES (3, 'c', 30000);
insert into PARTICIPANT_BALANCE (ID, NAME, BALANCE) VALUES (4, 'd', 40000);
insert into PARTICIPANT_BALANCE (ID, NAME, BALANCE) VALUES (5, 'e', 50000);

insert into PARTICIPANT_BALANCE (ID, NAME, BALANCE) VALUES (6, 'f', 60000);
insert into PARTICIPANT_BALANCE (ID, NAME, BALANCE) VALUES (7, 'g', 70000);'''

