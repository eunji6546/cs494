import sqlite3
from flask import g
from flask import Markup

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('test.db') #TODO: add your SQLite database filename
        db.row_factory = sqlite3.Row
    return db

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    get_db().execute('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return get_db()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except:
#     t.rollback()
#     raise
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select * from CurrentTime'
    results = query(query_string, one=True)
    #print(results)
    # alternatively: return results[0]['currenttime']
    return results['Time'] # TODO: update this as well to match the column name

# updates the current time as user selected.
def updateTime(new_time):
# TODO : update the database
    query_string = 'update CurrentTime Set Time = $new_time'
    results = query(query_string,{'new_time':new_time},one=True)
#print(results)
    return

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    try :
        query_string = 'select * from Item where itemID = $itemID'
    
        result = query(query_string, {'itemID': item_id}, one=True)
    except :
        result = None
#print("@")
    return result


def filter_bids(itemID, cate, fr, to, desc, status):
    
    from_table = ' Item '
    query_string = 'select * from'+ from_table
    curr = None
#results = query(query_string,{'fromTable':from_table)
    t = transaction()
    try :
        if ( itemID != ""):
        #from_table = 'select * from Item where item_ID = $itemID'
            query_string = 'select * from (' + query_string + ') where item_ID = $itemID'
    
        if ( fr != ""):
        #from_table = 'select * from Item where Buy_Price > $fr'
            query_string = 'select * from (' + query_string + ') where Buy_Price > $fr'
        if ( to != ""):
        #from_table = 'select * from Item where Buy_Price > $fr'
                query_string = 'select * from (' + query_string + ') where Buy_Price < $to'
# @ TODO : category, description substring...?, status
        if ( desc != ""):
            query_string = 'select * from ('+query_string +') where Description like "%'+desc+'%" '
        if ( status == 'open'):
            currenttime = query('select * from CurrentTime')[0]
            for temp in currenttime:
                curr = temp
#print(curr)
            query_string = 'select * from (' + query_string + ') where Started < $curr and Ends > $curr and (Buy_Price is Null or Buy_Price > Currently)'
        if ( status == 'closed'):
            currenttime = query('select * from CurrentTime')[0]
            for temp in currenttime:
                curr = temp
            query_string = 'select * from (' + query_string + ') where Started > $curr or Ends < $curr and (Buy_Price is Null or Buy_Price <= Currently)'
    
        query_string = 'select * from Category a inner join (' + query_string + ') as b on a.ItemID = b.ItemID'

        if (cate != ""):
            query_string = 'select * from ( '+ query_string + ') Where Caterogy = ' +cate
                #print(query_string)

        result = query(query_string, {'itemID':itemID, 'fr':fr,'to':to, 'curr':curr})

    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t.commit()
        return result

"""
    query_string = 'select * from Item'
    result = get_db.execute(query_string)
    if ( itemID != ""):
        query_string = 'select * '
        result = result.execute
    
    if ( fr != ""):
        #from_table = 'select * from Item where Buy_Price > $fr'
        query_string = 'select * from ' + query_string + 'where Buy_Price > $fr'
if ( to != ""):
    #from_table = 'select * from Item where Buy_Price > $fr'
    query_string = 'select * from ' + query_string + 'where Buy_Price < $to'
    if ( desc != ""):
        #from_table = 'select * from Item where Buy_Price > $fr'
        query_string = 'select * from ' + query_string + 'where Buy_Price < $to'
"""

def getBidsHtml(item):
    t = transaction()
    try :
        itemID = item['itemID']
        bids = query('Select * from Bids where itemID = $itemID', {'itemID':itemID})
        template = ' <p> <b>Bidder</b> %s bidded <b>$%s</b> at %s </p> <br>'
        html = '<p>'
        for a_bid in bids :
            html  = html + ' <b>Bidder</b> '+str(a_bid['BidderID'])+ ' bidded <b> $'+ str(a_bid['Amount'])+'</b> at '+str(a_bid['Time'])+ '<br>'
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t = commit()
        return Markup(html+'</p>')

def getBids(item):
    t = transaction()
    try:
        itemID = item['itemID']
        bids = query('Select * from Bids where itemID = $itemID', {'itemID':itemID})
        t = commit()
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t = commit()
        return bids

def validate_user(id):
    t = transaction()
    try:
        query_string = 'select * from User where UserID = $UserID'
        result = query(query_string, {'UserID':id})
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t = commit()

        return not isResultEmpty(result)

def validate_price(itemid, amount):
    t = transaction()

    query_string = 'select * from Item where ItemID = $itemID and Currently < $amount and (Buy_Price >= $amount or Buy_Price is Null) '
    result = query(query_string, {'itemID':itemid, 'amount':amount})
    return not isResultEmpty(result)

def validate_bidder(itemid, bidderid):
    t = transaction()
    try:
        query_string = 'select * from Bids where ItemID = $itemID and BidderID = $bidderid'
        result = query(query_string, {'itemID':itemid, 'bidderid':bidderid})

    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t = commit()
        return isResultEmpty(result)

def submit_bid(itemID, userID, amount):

    t = transaction()
    try:
        query_string = 'insert into Bids values("$ItemID", "$BidderID", "$Amount", $Time);'
    
        result = query(query_string, {'itemID':itemID, 'BidderID':userID,'amount':amount, 'Time':getTime()})
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t = commit()
        return

def find_winner(itemID):
    t = transaction()
    try:
        query_string = 'select * From Bids Where ItemID = $itemID Order by Amount desc'
        result = query(query_string, {'itemID':itemID})
        if isResultEmpty(result) :
            return None
        else :
            return result[0]
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t = commit()


# helper method to determine whether query result is empty
# Sample use:
# query_result = sqlitedb.query('select currenttime from Time')
# if (sqlitedb.isResultEmpty(query_result)):
#   print 'No results found'
# else:
#   .....
#
# NOTE: this will consume the first row in the table of results,
# which means that data will no longer be available to you.
# You must re-query in order to retrieve the full table of results
def isResultEmpty(result):
    try:
        result[0]
        return False
    except:
        return True

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}, one=False):
    cur = get_db().execute(query_string, vars)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
