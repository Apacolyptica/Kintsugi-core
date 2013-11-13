#!/usr/local/bin/python3

# print( "Content-Type: text/html")
# print( )

# import cgi, cgitb
# cgitb.enable()

import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD

session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

# form = cgi.FieldStorage()



# setup to connect to the Basex database
# set the search string provided by the HTML form
# search = str( form.getvalue( "search" ) )


#DCR: A pre-django page generator for our convenience

#DCR: This method takes the results from a variable number of searches
#DCR: ...and puts them into a single coherent page

def output(searchResults):

	#page = "<html><head><title>Test Page</title><meta http-equiv = \"Content Type\" \
	#content = \"text\\html; charset = utf-8\"></meta></head><body>"

	page = "TEST PAGE\n"
	for result in searchResults:
		page += ("\n\n" + result)
	page += "\n\n<!--This has been a search engine test-->\n"
	# page += "</body></html>"

	return page


try:

	#DCR: I am going to import the query externally in this example
	#DCR: Error handling is assumed to be handled externally

	def dbSearch(search, protoQuery):
		
		#DCR: Declared in and outside of the function because of scope technicalities
		session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

    		# connect to the Basex database
		session.execute("open cwec_v2-5")
		
		
    		# create a session for the title query
		query = session.query(protoQuery)

    		# bind the search variable to the query
		query.bind("$word", search)
		
    		# print results of the query within a table format
    		# print(query.execute()) is where the query is sent to the BaseX database and the result is printed
		
    		# print( "<p> Weaknesses with " + search + " in their name:</p><table>")
    		# print(query.execute())
    		# print( "</table>" )

		#result = "<br /><table>"
		#result += query.execute()
		#result += "</table>"
		
		result = query.execute()
    		# close the query/session
		query.close()
	
		return result
		
finally:
	if session:
		session.close()
