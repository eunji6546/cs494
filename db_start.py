#! usr/bin/python 
# -*- coding: utf-8 -*-

import MySQLdb as _mysql 
import sys 
import warnings

try:
    con = _mysql.connect('localhost', 'root', 'root', 'testdb')
    with con:
        cur = con.cursor()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            cur.execute("DROP TABLE IF EXISTS Writers")
            cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, \
		 Name VARCHAR(25))")
        cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
        cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
        cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
        cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
        cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")	
        con.query("Select version()")
    result = con.use_result()
    print "MySQL version: %s" % result.fetch_row()[0]
except _mysql.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1]) 
	sys.exit(1)

finally:
	if con :
		con.close()
	
