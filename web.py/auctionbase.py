#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
# current_time = string_to_time(sqlitedb.getTime())

def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

def merge(list1,list2):
    result = []
    if list1 == []:
       return list2
    elif list2 == []:
       return list1
    else:
       for x in list1:
          for y in list2:
             if x.ItemID == y.ItemID:
                    result.append(y)
       return result

#####################END HELPER METHODS#####################

urls = ('/currtime', 'curr_time',
        '/selecttime', 'select_time',
        # TODO: add additional URLs here
        # first parameter => URL, second parameter => class name
        '/add_bid','add_bid',
        '/search','search',
        '/info(.*)','info',
        )

class curr_time:
    # A simple GET request, to '/currtime'
    #
    # Notice that we pass in `current_time' to our `render_template' call
    # in order to have its value displayed on the web page
    def GET(self):
        current_time = sqlitedb.getTime()
        return render_template('curr_time.html', time = current_time)

class select_time:
    # Aanother GET request, this time to the URL '/selecttime'
    def GET(self):
        
        return render_template('select_time.html')

    # A POST request
    #
    # You can fetch the parameters passed to the URL
    # by calling `web.input()' for **both** POST requests
    # and GET requests
    def POST(self):
        post_params = web.input()
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss'];
        enter_name = post_params['entername']


        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        # TODO: save the selected time as the current time in the database
        t = sqlitedb.transaction()
        try:
          sqlitedb.setTime(selected_time) 
        except Exception as e:
           t.rollback()
           print str(e)
           update_message = str(e)
        else:
            t.commit()
        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)
class add_bid:
    def GET(self):
        return render_template('add_bid.html')
    def POST(self):
        params = web.input()
        itemID = int(params['itemID'])
        userID = params['userID']
        price = params['price']
        currentTime = sqlitedb.getTime()
        update_message = 'You(userID:%s) have successfully bidded on the item(itemID:%s) for %s dollars'% (userID, itemID, price)
        t = sqlitedb.transaction()
        try:
           sqlitedb.addBid(itemID, userID, price,currentTime)
        except Exception as e:
           t.rollback()
           print str(e)
           update_message = str(e)
           return render_template('add_bid.html',message = update_message, add_result = False)
        else:
            t.commit()   
            return render_template('add_bid.html', message = update_message, add_result = True)

class search:
    def GET(self):
        return render_template('search.html')
    def POST(self):
        params = web.input()
        itemID = params['itemID']
        userID = params['userID']
        minPrice = params['minPrice']
        maxPrice = params['maxPrice']
        status = params['status']
        category = params['category']
        description = params['description']
        currTime = sqlitedb.getTime()       

        if itemID != "":
           t = sqlitedb.transaction()
           result1 = sqlitedb.getItemByStatus(status,currTime)
           try:
              myresult = sqlitedb.getItemById(itemID)
           except Exception as e:
              t.rollback()
              print str(e)
              update_message = 'No item found.'
              
              return render_template('search.html', search_result = False, message = update_message)
           else:
              t.commit()
              result = merge(myresult,result1)
              return render_template('search.html', search_result = result)
        else:
           t = sqlitedb.transaction()
           try:
              result1 = sqlitedb.getItemByUserID(userID)
              result2 = sqlitedb.getItemByPrice(minPrice,maxPrice)
              result3 = sqlitedb.getItemByStatus(status,currTime)
              result4 = sqlitedb.getItemByCategory(category)
              result5 = sqlitedb.getItemByDescription(description)
           except Exception as e:
              t.rollback()
              print str(e)
              return render_template('search.html',message = str(e))
           else:
              m1 = merge(result1,result2)
              m2 = merge(m1,result3)
              m3 = merge(m2,result4)
              result = merge(m3,result5)
              if result == []:
                 update_message = 'No Item found.'
                 return render_template('search.html',message = update_message)
              else:
                 return render_template('search.html',search_result = result)

class info:
     def GET(self,itemID):
         mes = ""+itemID
         itemID = mes.replace("/","")
         currentTime = sqlitedb.getTime()
         status = sqlitedb.status(itemID,currentTime)
         result = sqlitedb.bids(itemID)
         
         if status == "open":
            return render_template('info.html',information = status,search_result = result)
         elif status == "closed":
            win = sqlitedb.winner(itemID)
            if len(win) != 0:
               Winner = win[0].UserID
            else:
               Winner = ""
            return render_template('info.html',information = status,search_result = result,winner = Winner)
###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
