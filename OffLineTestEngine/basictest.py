#!/usr/local/bin/python3

# print( "Content-Type: text/html")
# print( )

# import cgi, cgitb
# cgitb.enable()

import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD

session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

# The core of this method is just the search engine

# Opening web-forms (will modify as necessary for the Djangofication

# form = cgi.FieldStorage()

# setup to connect to the Basex database
# set the search string provided by the HTML form
# search = str( form.getvalue( "search" ) )


#DCR: A pre-django page generator for our convenience

#This is a deprecated method for test purposes only
#This method prints the output to the console after shaving blanks

def output(searchResults):
	#page = "TEST PAGE\n"
	page = ""
	for result in searchResults:
		if result:
			page += result
	return page

try:

	# I am going to import the query externally
	# Error handling is assumed to be handled externally

	#This method takes in the search string and the query to be run
	#The search is treated as a variable in the BaseX query
	#This method returns the results of that query
	def dbSearch(search, protoQuery):
		
		#DCR: Declared in and outside of the function because of scope technicalities
		session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

    		# connect to the Basex database
		session.execute("open cwec_v2-5")
		
		
    		# create a session for the title query
		query = session.query(protoQuery)

    		# bind the search variable to the query
		query.bind("$word", search)
		
		# Execute the query
		result = query.execute()

    		# close the query/session
		query.close()
	
		return result
		
finally:
	if session:
		session.close()
