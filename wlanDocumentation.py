import sys
import subprocess
import os
import datetime 
import sqlite3
import time

conn = sqlite3.connect("Heimkehrdb.sqlite")
cur = conn.cursor()

cur.executescript("""

DROP TABLE IF EXISTS Heimkehre;
DROP TABLE IF EXISTS Ausgänge;
DROP TABLE IF EXISTS Auflistung;

CREATE TABLE Heimkehre (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    zeiten   TEXT UNIQUE);
    
CREATE TABLE Ausgänge (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    zeiten   TEXT UNIQUE);

CREATE TABLE Auflistung (
    Ausgang   TEXT UNIQUE,
    Rückkehr   TEXT UNIQUE
)
    """)



ip_Network = ("IP_NETWORK")
ip_device = ("add here the ip of your divice,which you want observe") 

proc = subprocess.Popen("ping " + ip_device , shell=True, stdout = subprocess.PIPE)

status = [1, 2, 3]  
i  = 2
q = 1 

while True:


    output = proc.stdout.readline()
    print("line" + str(output))

    print(status[i], status[i-1])
    if str(status[i]) == "b'bytes'" and str(status[i]) != str(status[i-1]):
        print("connected")
        time1 = str(datetime.datetime.now())
        cur.execute("""
        INSERT OR IGNORE INTO Heimkehre (zeiten) VALUES (?)""", ( time1, ) ) 
        print("inserted in Heimkehre")
        print(time1)

        cur.execute('SELECT zeiten FROM Heimkehre WHERE id = ? ', (q, ))
        Rückkehr = cur.fetchone()[0]

        cur.execute('''
        INSERT OR IGNORE INTO Auflistung (Rückkehr) VALUES (?)''', (Rückkehr, ))
        print("inserted in Auflistung")
        conn.commit()
    

    if str(status[i]) == "b'timeout'" and str(status[i]) != str(status[i-1]):
        print("entkoppelt")
        time2 = str(datetime.datetime.now())
        cur.execute('''
        INSERT OR IGNORE INTO Ausgänge (zeiten) VALUES (?)''', (time2, ) )
        print("inserted in Ausgänge")
        print(time2)

        cur.execute('SELECT zeiten FROM Ausgänge WHERE id = ? ', (q, ))
        Ausgang = cur.fetchone()[0]

        cur.execute('''
        INSERT OR IGNORE INTO Auflistung (Ausgang) VALUES (?)''', (Ausgang, ))
        print("inserted in Auflistung")
        q = q + 1
        conn.commit()

    info = output.split()[1]
    status.append(info)
    print(status)
    status.remove(status[i-2])
    #i = i + 1 

    #time.sleep(2)


