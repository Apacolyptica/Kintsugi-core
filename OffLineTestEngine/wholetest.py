#!/usr/local/bin/python3

import qGen
import sys
import basictest
import ranking

if (len(sys.argv) < 2):
	print("Usage " + sys.argv[0] + " search-term")
	print("Example: " + sys.argv[0] + " buffer")

#this is a placeholder until CGI-forms comes in
search = sys.argv[1]


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
	_list = []
	queryType = -1
	#-1 = ID query
	#0 = Name query
	#1 = full-text query
	#These are done in descending order of priority
	while queryType < 2:
		temp = qGen.makeQuery(queryType, filters[0], filters[1])
		_list.append(temp)
		queryType += 1
	return _list

def process_query(search_term, q_list):
	result = False
	for query in query_list:
		#run the query amd get the results
		temp = basictest.dbSearch(search_term,query)
		
		#format the results for processing the ranking algorithm
		temp = ranking.process_input(temp)
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


query_list = make_query_list(filters)
output = process_query(search, query_list)
output = ranking.r_sort(output)
output = ranking.process_output(output)
print(output)
