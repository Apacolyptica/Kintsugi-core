#!/usr/bin/env python3

"""
Generates search result pages.
"""

import result_queries
import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD
#import sys

def concat_query_make(query_ends):
	"""This method concatenates several queries whose node returns a single value 
	DELIM is used as the delimiter between conatenated entries."""

	query = result_queries.START
	start = True

	if query_ends:
		for end in query_ends:
			if start:
				query += end
				#end is the varying return value to an otherwise identical query


			if not start:
				query += " || \"DELIM\" || "
				query += end
	
			start = False
			
	else:
		query = "(no query selected)"
	
	return query

def search(queries, session, is_relation, term):
	"""
	This method runs a given query in BaseX and returns the result text 
	For the sake of formatting, CWE relationships are handled a little differently
	"""

	page = ""
	temp_list = []
	final_page = ""
	for query in queries:
		if(is_relation):
			query = result_queries.START + query

		query = session.query(query)
		query.bind("$word", term)
		temp = query.execute()
		query.close()

		#Because of stupidity with the relational part of the database
		#The relational output is handled a little differenty

		#ALGO If the query involves a CWE relationship
		if(is_relation):
			temp_list.append(temp.split(" "))
			#print(temp_list)
			page = temp_list
		else:
			page = temp
		#This will produce 3 lists of identical length
		
	#If the lengths are not identical, we have a problem, so we'll make sure
	if(is_relation):
		final_page = format_relation_data(page, session)
	else:
		#May need to replace this with a djangofied method
		final_page = page.replace("DELIM", "<br/><br/>")
	
	return final_page
	
def format_relation_data(page, session):
	"""
	This method is is a temporary method to convert the CWE relationship data into a table
	This method will be depricated by a django template in the future
	The input data is a list of lists, the sub-lists are all of equal length.
	The sub-lists are the Relationship Category, Nature, and CWE identity.
	Each sub lists index corresponds with the other (page[0][0], page[1][0], page[2][0] are the first relationship)
	THIS METHOD WILL BE DEPRACATED ONCE A PROPER DJANGO TEMPLATE IS IMPLEMENTED
	"""

	LINK_START ="http://kintsugi.nucia.unomaha.edu/cwe/"
	#PUT AN ERROR CODE HERE?
	final_page = "Unexpected error in data processing"

	#TODO: Refactor "table script" to use django templates if possible
	#ALGO: Converts the list-of-lists into a customizxed table
	if(len(page[0]) == len(page[1]) and len(page[1]) == len(page[2])):
		final_page = "<div class=\"relationships\"><h3>Relationships</h3><table><thead><tr><th>Relationship<br/>Category</th><th>Relationship<br/>Nature</th><th id=\"cweTitle\">CWE Title</th></tr></thead>"
		for i in range(len(page[0])):
			final_page += "<tr><td>" + page[0][i] + "</td><td>" + page[1][i] + "</td>"
			final_page += "<td id=\"cweTableName\">" + "<a href = \"" + LINK_START + page[2][i] + "\">"
			final_page += nameLookup(page[2][i],session) + "</a></td></tr>"
		final_page += "</table></div>"

	return final_page

def nameLookup(term, session):
	"""
	This method looks up the name of a given CWE ID.  The purpose of this method is to provide the name in
	the CWE relationship display, which is not in the relationship sub-entries in the database
	"""

	#IDEA: To improve scalability, implement a "shadow" database with only ID's and names for this method (Given its frequency of evocation)
	#If the output stays "ERROR" We can put an error code or something"
	query = result_queries.START + "data($v/@Name)"
	#query = "declare variable $word external; for $v in//*[@ID = $word] return data($v/@Name)"
	output = "ERROR"
	query = session.query(query)
	query.bind("$word", term)
	output = query.execute()
	query.close()
	return output
	
def run_result_page(quest_item):
	session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)
	session.execute("open cwec_v2-5")
	
	#the next method expects a list, so this appeases that expectation with
	#minimal redundant code
	concat_query = [concat_query_make(result_queries.RETURN)]
	cwe_result_out = "<p>" # Added by Chris
	cwe_result_out = cwe_result_out + search(concat_query, session, False, quest_item)
	cwe_result_out = cwe_result_out + "</p>" # Added by Chris
	#cwe_result_out = cwe_result_out + "<br /><br />"
	cwe_result_out = cwe_result_out + "<p>" # Added by Chris
	cwe_result_out = cwe_result_out + search([result_queries.ALT_TERM], session, False, quest_item)
	cwe_result_out = cwe_result_out + "</p>" # Added by Chris
	#cwe_result_out = cwe_result_out + "<br /><br />"
	cwe_result_out = cwe_result_out + search(result_queries.RELATION, session, True, quest_item)
	#cwe_result_out = cwe_result_out + "<br /><br />"
	cwe_result_out = cwe_result_out + "<a id=\"mitreRef\" href = \"http://cwe.mitre.org/data/definitions/" + quest_item + ".html\">See Mitre's site for more information</a>"
	session.close()
	
	return cwe_result_out
