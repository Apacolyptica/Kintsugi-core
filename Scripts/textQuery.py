#!/usr/local/bin/python3

print( "Content-Type: text/html")
print( )

import cgi, cgitb
cgitb.enable()

import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD

form = cgi.FieldStorage()

print( "<body>" )

form = cgi.FieldStorage()

session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

search = str( form.getvalue( "search" ) )

try:
    session.execute("open cwec_v2-5")

    textQuery = "for $v in //Weakness_Catalog/Weaknesses/Weakness[. contains text \"" + search + "\" ]  \
                   return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

    nameQuery = "for $v in //Weakness_Catalog/Weaknesses/Weakness[@Name[. contains text \"" + search + "\" ] ] \
                    return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

    query = session.query(nameQuery)

    print( "<p> Weaknesses with " + search + " in their name:</p><table>")
    print(query.execute())
    print( "</table>" )

    query.close()

    query = session.query(textQuery)

    print( "<p>Weaknesses with " + search + " in their text:</p><table>")
    print(query.execute())
    print( "</table>" )

    query.close()

finally:
    if session:
        session.close()

print( "</body>" )