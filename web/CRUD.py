#!flask/bin/python
from flask import render_template
from flask import Flask
from flask import Flask,request
from flask import render_template
import MySQLdb as mdb
import sys

app = Flask(__name__)
"""
try:
	con = mdb.connect('localhost', 'root', 'root', 'testdb');

	with con:

		cur = con.cursor()
		
		#Create
		cur.execute("DROP TABLE IF EXISTS Writers")
		cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
		
		for i in range(100):
			cur.execute("INSERT INTO Writers(Name) VALUES('" + str(i) + "')")

				#Update all
		cur.execute("UPDATE Writers SET Name='Unknown' WHERE Id>0")

		#Retrieve Again
		cur.execute("SELECT * FROM Writers")

		for i in range(cur.rowcount):
			row = cur.fetchone()
			print row[0], row[1]

		#Delete
		cur.execute("DELETE FROM Writers WHERE Name='Unknown'")
		
		#Retrieve Again
		cur.execute("SELECT * FROM Writers")
		for i in range(cur.rowcount):
			row = cur.fetchone()
			print row[0], row[1]

	cur = con.cursor()
	cur.execute("SELECT VERSION()")

	ver = cur.fetchone()
	print "Database version : %s " % ver

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)

finally:
	if con:
		con.close()
"""
def getnum() :
    total_number = -1
    print("counting number")
    try:
        con = mdb.connect('localhost', 'root', 'root', 'testdb');
        
        with con:
            
            cur = con.cursor()
            cur.execute("SELECT * FROM Writers")
            """
                for i in range(cur.rowcount):
                row = cur.fetchone()
                print row[0], row[1]
                """
            total_number = cur.rowcount
    

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    print(total_number)
    return total_number

@app.route('/')
def hello():
    
    try:
        con = mdb.connect('localhost', 'root', 'root', 'testdb');
        
        with con:
            
            cur = con.cursor()
            #Retrieve
            cur.execute("DROP TABLE IF EXISTS Writers")
            cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
            
            cur.execute("SELECT * FROM Writers")
            """
            for i in range(cur.rowcount):
                row = cur.fetchone()
                print row[0], row[1]
            """
            total_number = cur.rowcount
            print(total_number)

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if con:
            con.close()

    return render_template('index.html', total_number = total_number, message = "")

@app.route('/insert_data', methods=['GET', 'POST'])
def insert_data():
    number = -1
    message = "FUCKYOU"
    if request.method == 'POST':
        post_params = request.form
        method = post_params['method']
        
        if method == 'insert':
            print("insert called")
            try:
                con = mdb.connect('localhost', 'root', 'root', 'testdb');
                
                with con:
                    cur = con.cursor()
                    for i in range(100):
                        cur.execute("INSERT INTO Writers(Name) VALUES('" + str(i) + "')")
    
    
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
            
            finally:
                message = "insert complete"
                if con:
                    con.close()
    number = getnum()
    return render_template('insert_data.html', total_number = number, message = message)

@app.route('/delete_data', methods=['GET', 'POST'])
def delete_data():
    number = -1
    message = "FUCKYOU"
    if request.method == 'POST':
        post_params = request.form
        method = post_params['method']
        
        if method == 'delete':
            print("delete called")
            try:
                con = mdb.connect('localhost', 'root', 'root', 'testdb');
                
                with con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM Writers WHERE Name='Unknown'")
    
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
            
            finally:
                message = "delete complete"
                if con:
                    con.close()
    number = getnum()
    return render_template('delete_data.html', total_number = number, message = message)


@app.route('/update_data', methods=['GET', 'POST'])
def update_data():
    number = -1
    message = "FUCKYOU"
    if request.method == 'POST':
        post_params = request.form
        method = post_params['method']
        
        if method == 'update':
            print("update called")
            try:
                con = mdb.connect('localhost', 'root', 'root', 'testdb');
                
                with con:
                    cur = con.cursor()
                    cur.execute("UPDATE Writers SET Name='Unknown' WHERE Id>0")
    
            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
            
            finally:
                message = "update complete"
                if con:
                    con.close()
    number = getnum()
    return render_template('update_data.html', total_number = number, message = message)





@app.route('/index', methods=['GET', 'POST'])
def index() :
    if request.method == 'POST':
        print("!!!!")
        return render_template('index.html', total_number=getnum(), message="")
    else :
        return render_template('index.html', total_number=getnum(), message="")
if __name__ == '__main__':
    app.run(host='0.0.0.0')
