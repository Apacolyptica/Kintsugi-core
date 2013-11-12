#!/usr/local/bin/python3

print( "Content-Type: text/html")
print( )

import cgi, cgitb
cgitb.enable()

import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD

from queryList import nameQuery, textQuery
from queryDef import bQuery

form = cgi.FieldStorage()

# setup to connect to the Basex database
session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

# set the search string provided by the HTML form
search = str( form.getvalue( "search" ) )

try:
    # connect to the Basex database
    session.execute("open cwec_v2-5")

    print( "<table>" )

    print( "<tr><td><h2>Results with " + search + " in the title</h2></td></tr>" )

    bQuery(search, session.query(nameQuery))

    print( "<tr><td><h2>Results with " + search + " in the text</h2></td></tr>" )

    bQuery(search, session.query(textQuery))

    print( "</table>" )

    # close the query/session
    #query.close()

finally:
    if session:
        session.close()
