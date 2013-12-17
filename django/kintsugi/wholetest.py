#!/usr/bin/env python3

import qGen
#import sys
#import basictest
import search_engine
    
#This is the queries searched in descending order of rank
#"False" is the full text search
RANKING = ["ID", "Name", False]

#A default placeholder for the field value
#This will be replaced with user-input for what field to search
FIELD = False

filters = (0,0) #default filter tuple
#current format for filters is ([list] [[list-of-lists]])
#plan to refactor to a better format later
#example of filters
#filters = (["Langauge_Name"],[["C"]])"
#filters = (["Langauge_Name", "Operating System Name"] \
	#, [["C", "C++", "Java"], ["Windows_Vista"]])
#if the argument is 0, that indicates no filter


#Here is a list of 3 queries (assuming no arguments for now)

def make_query_list(filters):
	"""
	This method dynamically generates the queries according to filters and rank priority
	"""
	_list = []
	#-1 = ID query
	#0 = Name query
	#1 = full-text query
	#These are done in descending order of priority
	for queryType in RANKING:
		temp = qGen.makeQuery(FIELD, queryType, filters[0], filters[1])
		_list.append(temp)
		#queryType += 1
	return _list

def process_query(search_term, q_list):
	"""
	This method runs the queries through the search engine and
	converts the output to a 3-deep list
	The 3-deep list works as follows
	The top "layer" is the master list
	The middle later is the results of a given query
	The bottom later is said results split into ordered pairs
	(these results are split [CWE_ID, CWE_NAME])
	"""
	result = False
	for query in q_list:
		#run the query amd get the results
		temp = search_engine.dbSearch(search_term,query)

		#format the results for processing the ranking algorithm
		temp = search_engine.process_input(temp)
		#print(temp)
		#convert the whole series into a 3-deep list
		#The first level is the entire list
		#The second level is the sub-list of the query result
		#The third level are "ordered pairs" of each individual result...
		#...of the list of results the query returned
		if result:
			result.append(temp)
		else:
			result = [temp]
		#print(temp)
	#result = basictest.output(result)
	return result


def run_wholetest(search):
	"""
	This is the overall script that runs the search engine and processes the output
	This is effectively the "main" method of the overall search engine
	"""
	query_list = make_query_list(filters)
	output = process_query(search, query_list)
	output = search_engine.r_sort(output)
	return output
