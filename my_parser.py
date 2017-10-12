

"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file,f,C,B1,U):
    with open(json_file, 'r') as m:
        items = loads(m.read())['Items'] # creates a Python dictionary of Items for the supplied json file       
        
           
        for item in items:
             ID=item['ItemID']
             name=item['Name']
             Ca=item['Category']
             De=item['Description']
             name = escape(name)
             De = escape (str(De))
             f.write(ID)
             f.write('|')

             for m in Ca:
                 m = escape(m)
                 C.write(ID)
                 C.write('|')
                 C.write(m)
                 C.write('\n')
                  
             star = item['Started']
             end = item['Ends']
             star = escape(star)
             end = escape(end)
             star=transformDttm(star)
             end= transformDttm(end)
             star = escape(star)
             end = escape(end)
  
             num = item['Number_of_Bids']
             current = item['Currently']
             current = escape(current)
             current = transformDollar(current)
             current = escape(current)
      
             seller=item['Seller']
             Lo = item['Location']
             Co = item['Country']
             SID= seller['UserID']
             Srating = seller['Rating']
             SID = escape(SID)
             Lo=escape(Lo)
             Co=escape(Co) 
               
             f.write(SID)
             f.write('|')
             f.write(name)
             f.write('|')
             U.write(SID)
             U.write('|')
             U.write(Srating)
             U.write('|')
             U.write(Lo)
             U.write('|')
             U.write(Co)
             U.write('\n')
             
             if 'Buy_Price' in item:
                 BuyPrice = item['Buy_Price']
                 BuyPrice = escape(BuyPrice)
                 BuyPrice = transformDollar(BuyPrice)
                 BuyPrice = escape(BuyPrice)
             else:
                 BuyPrice = 'NULL'
             FirstBid = item['First_Bid']
             FirstBid = escape(FirstBid)
             FirstBid = transformDollar(FirstBid)
             FirstBid = escape(FirstBid)
  
             f.write(BuyPrice)
             f.write('|')
             f.write(FirstBid)
             f.write('|')
             f.write(current)
             f.write('|')
             f.write(num)
             f.write('|')
             f.write(star)
             f.write('|')
             f.write(end)
             f.write('|')
             f.write(De)
             f.write('\n')

             Bi = item['Bids']
             if Bi != None:                  
                    for a in Bi:
                       bid = a['Bid']        
                       bidder = bid['Bidder']
                       bID = bidder['UserID']
                       brating = bidder['Rating']
                       if 'Location' in bidder:
                         bLo = bidder['Location']
                       else:
                         bLo = 'NULL'
                       if 'Country'  in bidder:
                         bCo = bidder['Country']
                       else:
                         bCo = 'NULL'
                       bCo = escape(bCo)
                       bLo = escape(bLo)
                       bID = escape(bID)
                       
                       U.write(bID)
                       U.write('|')
                       U.write(brating)
                       U.write('|')
                       U.write(bLo)
                       U.write('|')
                       U.write(bCo)
                       U.write('\n')
                  
                       amountB = bid['Amount']
                       timeB = bid['Time']
                       amountB = transformDollar(amountB)
                       timeB = transformDttm(timeB)
                       amountB = escape(amountB)
                       timeB = escape(timeB)
                       B1.write(ID)
                       B1.write('|')
                       B1.write(bID)
                       B1.write('|')
                       B1.write(amountB)
                       B1.write('|')
                       B1.write(timeB)
                       B1.write('\n')
        
def escape(str):
    if str.find('"') != -1:
      str = str.replace('"','""')
      l = list(str)
      
      l.insert(0,'"')
      l.append('"')  
      newS = ''.join(l)
      return newS
    else:
      return str
             

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    f=open('Item.dat','w')
    C = open('CategoryOf.dat','w')
    B1 = open('MakeBids.dat','w')
    U = open('User.dat','w')
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for m in argv[1:]:
        if isJson(m):
            parseJson(m,f,C,B1,U)
            print "Success parsing " + m

if __name__ == '__main__':
    main(sys.argv)


