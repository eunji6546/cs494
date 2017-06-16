import sys

from flask import Flask
from flask import request
from flask import render_template

import sqlitedb
from datetime import datetime

app = Flask(__name__)

"""""""""""""""""""""""""""""""""""""""""""""""""""
!!!!!DO NOT CHANGE ANYTHING ABOVE THIS LINE!!!!!
"""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""
BEGIN HELPER METHODS
"""""""""""""""""""""""""""""""""""""""""""""""""""


def string_to_time(date_str):
    """Helper method to convert times from database (which will return a string) into datetime objects.

    This will allow you to compare times correctly (using # ==, !=, <, >, etc.) instead of
    lexicographically as strings.

    >>> current_time = string_to_time(sqlitedb.getTime())
    """
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


"""""""""""""""""""""""""""""""""""""""""""""""""""
END HELPER METHODS
"""""""""""""""""""""""""""""""""""""""""""""""""""


@app.route('/currtime', methods=['GET'])
def get_curr_time():
    """A simple GET request, to '/currtime'.

    Notice that we pass in `current_time' to our `render_template' call
    in order to have its value displayed on the web page
    """
    
    
    current_time = sqlitedb.getTime()
    #print(current_time)
        
    


    return render_template('curr_time.html', time=current_time)


@app.route('/selecttime', methods=['GET', 'POST'])
def select_time():
    if request.method == 'POST':
        # A POST request
        #
        # You can fetch the parameters passed to the URL
        # by calling `request.form' for POST requests
        post_params = request.form
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss']
        enter_name = post_params['entername']

        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        # TODO: save the selected time as the current time in the database
        sqlitedb.updateTime(selected_time)

        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)
    else:
        return render_template('select_time.html')


"""""""""""""""""""""""""""""""""""""""""""""""""""
IMPLEMENT OTHER FEATURES IN HERE
"""""""""""""""""""""""""""""""""""""""""""""""""""
@app.route('/bidlist', methods=['GET', 'POST'])
def bid_list():
    
    if request.method == 'POST':
        error = None
        post_params = request.form
        itemID = post_params['itemID']
        cate = post_params['category']
        fr = post_params['from']
        to = post_params['to']
        desc = post_params['description']
        status = post_params['status']
        if fr != "" and to != "" and fr>to :
            error = " 'to' have to be bigger than 'from'"
            return render_template('bid_list.html',error=error)
        else :
            #error = "Filtered Result Below"
            result = sqlitedb.filter_bids(itemID, cate, fr, to, desc, status)
            currtime = sqlitedb.getTime()
            
            biddingList = []
            statusList = []
            winnerList = []
            for item in result :
                started = item['Started']
                ends = item['Ends']
                currently = item['Currently']
                buy_price = item['Buy_Price']
                
                if started < currtime and ends > currtime and (buy_price == None or float(currently) < float(buy_price)) :
                    statusList.append(True)
                    winnerList.append(None)
                else :
                    statusList.append(False)
                    winnerList.append(sqlitedb.find_winner(item['itemID']))
                biddingList.append(sqlitedb.getBids(item))
        
        
            return render_template('bid_list.html', itemList = result, statusList = statusList, biddingList = biddingList, winnerList=winnerList )
    else :
        return render_template('bid_list.html' )


@app.route('/submitBid', methods=['GET', 'POST'])
def submit_bid() :
    if request.method == 'POST':
        post_params = request.form
        userID = post_params['userID']
        itemID = post_params['itemID']
        amount = post_params['amount']
        validity = sqlitedb.validate_user(userID)
        if validity :
            validity = sqlitedb.validate_price(itemID, amount)
            if not validity :
                return render_template('message.html', message = "Your Price is invalid (Larger than BuyPrice or smaller than Current largest bidding amount)")
            else :
                validity = sqlitedb.validate_bidder(itemID, userID)
                if validity:
                    sqlitedb.submit_bid(itemID, userID, amount)
                    return render_template('message.html', message = "Successfully submitted")
                else :
                    return render_template('message.html', message= "You already bidded to this item")
        else :
            msg = "Your ID is invalid"
            return render_template('message.html', message = msg)


    return render_template('bid_list.html')
"""""""""""""""""""""""""""""""""""""""""""""""""""
!!!!!DO NOT CHANGE ANYTHING ABOVE THIS LINE!!!!!
"""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == '__main__':
    port = 5000 if len(sys.argv) == 1 else int(sys.argv[1])
    app.run(port=port)
