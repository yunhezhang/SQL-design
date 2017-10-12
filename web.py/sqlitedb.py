import web

db = web.database(dbn='sqlite',
        db='AuctionBase.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select CurTime from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].CurTime # TODO: update this as well to match the
                                  # column name

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Items where ItemID = $itemID'
    result = query(query_string, {'itemID': item_id})
    
    try:
        check = result[0]
    except len(result) == 0:
      print ('No Item found.')
    else:
      return result

def getItemByUserID(user_id):
    if user_id == "":
       result = []
    else:
       query_string = 'select * from Items where UserID = $userID'
       result = query(query_string,{'userID':user_id})
    return result

def getItemByPrice(minPrice,maxPrice):
    if minPrice == "" and maxPrice == "":
        result = []
    elif minPrice == "":
        query_string = 'select * from Items where Currently <= $max_price'
        result = query(query_string,{'max_price':maxPrice})
    elif maxPrice == "":
         query_string = 'select * from Items where Currently >= $min_price '
         result = query(query_string,{'min_price':minPrice})
    else:  
         query_string = 'select * from Items where Currently >= $min_price and Currently <= $max_price'
         result = query(query_string,{'min_price':minPrice,'max_price':maxPrice})
    return result

def getItemByStatus(status,currTime):
    if status == "open":
         query_string = 'select * from Items where Started <= $current and Ends >= $current and Currently < Buy_Price'
         result = query(query_string,{'current':currTime})
    elif status == "close":
         query_string = 'select * from Items where Ends < $current or Currently >= Buy_Price'
         result = query(query_string,{'current':currTime})
    elif status == "notStarted":
         query_string = 'select * from Items where Started > $current'
         result = query(query_string,{'current':currTime})
    elif status == "all":
         query_string = 'select * from Items'
         result = query(query_string)
    return result

def getItemByCategory(cate):
    if cate == "":
       result = []
    else:
       query_string = 'select * from Items, Categories  where Items.ItemID = Categories.ItemID and Categories.Category = $category'
       result = db.query(query_string,vars = {'category':cate})
    return result

def getItemByDescription(des):
    if des == "":
       result = []
    else:
       query_string = 'select * from Items where Description LIKE $description'
       result = db.query(query_string,vars = {'description' : '%'+des+'%'})
    return result

def status(itemID, currentTime):
    status = ""
    query_string = 'select * from Items where ItemID = $item_id and Ends <= $currTime'
    result = query(query_string, {'item_id':itemID,'currTime':currentTime})
    if len(result) == 0:
        status = "open"
    else:
        status = "closed"
    return status

def bids(itemID):
    result = []
    query_string = 'select UserID,Amount,Time from Bids where ItemID = $item_id'
    result = query(query_string,{'item_id':itemID})
    return result
def winner(itemID):
    query_string = 'select B.UserID from Bids B,Items I where B.ItemID = $item_id and B.ItemID = I.ItemID and B.Amount = I.Currently'
    result = query(query_string,{'item_id':itemID})
    return result 
  
# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
def setTime(selected_time):
   query_string = 'update CurrentTime set CurTime = $current'
   db. query(query_string,vars =  {'current': selected_time}) 
def addBid(itemID,userID,price,currentTime):
   query_string = 'Insert into Bids values($ItemID,$UserID,$Amount,$Time)'
   db.query(query_string,{'ItemID':itemID,'UserID':userID,'Amount':price,'Time':currentTime}) 
