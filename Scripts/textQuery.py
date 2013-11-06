#!/usr/local/bin/python3

print( "Content-Type: text/html")
print( )

import cgi, cgitb
cgitb.enable()

import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD

form = cgi.FieldStorage()

print( "<body>" )

# setup to connect to the Basex database
session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

# set the search string provided by the HTML form
search = str( form.getvalue( "search" ) )

try:
    # connect to the Basex database
    session.execute("open cwec_v2-5")

    # query for the string within the title
    # searching within Weaknesses for a match in the element name
    #         returns the ID # and the Name of the database entry with HTML table row format
    nameQuery = "for $v in //Weakness_Catalog/Weaknesses/Weakness[@Name[. contains text \"" + search + "\" ] ] \
                    return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

    # create a session for the title query
    query = session.query(nameQuery)

    # print results of the query within a table format
    # print(query.execute()) is where the query is sent to the BaseX database and the result is printed
    print( "<p> Weaknesses with " + search + " in their name:</p><table>")
    print(query.execute())
    print( "</table>" )

    # close the query/session
    query.close()

    # query for the string located within the text
    # search within the Weaknesses for a match in the element's text
    #         returns the ID # and the Name of the database entry with HTML table row format
    textQuery = "for $v in //Weakness_Catalog/Weaknesses/Weakness[. contains text \"" + search + "\" ]  \
                   return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

    # create a session for the text query
    query = session.query(textQuery)

    # print the results of the query within a table format
    # print(query.execute()) is where the query is sent to the BaseX database and the result is printed
    print( "<p>Weaknesses with " + search + " in their text:</p><table>")
    print(query.execute())
    print( "</table>" )

    # close the query/session
    query.close()

finally:
    if session:
        session.close()

print( "</body>" )