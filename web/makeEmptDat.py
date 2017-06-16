import sys 
from re import sub 

columnSeparator = "|"


bids = open('bids_table.dat','a');
categorys = open('category_table.dat','a');
items = open('item_table.dat','a');
users = open('user_table.dat','a');
currtimes = open('currenttime_table.dat','a');

bids.close();
categorys.close();
items.close();
users.close();
currtimes.close();

