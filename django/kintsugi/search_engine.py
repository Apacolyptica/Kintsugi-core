#!/usr/bin/env python3

"""
Search engine query and formatting functions.
"""

import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD


#This is a deprecated method for test purposes only
#This method prints the output to the console after shaving blanks

def output(searchResults):
	"""
	DEPRECATED: This is a test mthod to test the output of the search engine
	This was made obsolete once 'wholetest' was created
	"""
	#page = "TEST PAGE\n"
	page = ""
	for result in searchResults:
		if result:
			page += result
	return page



#This method takes in the search string and the query to be run
#The search is treated as a variable in the BaseX query
#This method returns the results of that query
def dbSearch(search, protoQuery):
	"""
	This method takes in a BaseX search query and a term to be searched for
	The search is ran through BaseX and its value returned
	"""
		
	# Declare the BaseX session
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
	session.close()
	return result
		

def format_result_list(_inList):
    """
    This method takes a list of strings returned and processed from the search query
    This method splits the ID and Name of each entry, returning a list of lists to more easily work with
    """
    result = []
    for entry in _inList:
        if entry:
            #Split the ID number and name of the CWE entry
            temp = entry.split(" ", 1)

            #Append the new list to rhe resulting list of lists
            result.append(temp)

    #Sort the results by ID number
    result = sorted(result, key=lambda result: int(result[0]))

    return result

#This method is a classic binary search
#This is performed on the ID portion of the CWE list
#This is used to ensure no duplicate entries in the final output

def bSearch(_inList, target, min_num, max_num):
    """
    This method is the classic binary search applied to CWE ID numbers
    It takes the ID number in a CWE and searches its presence in the master list
    This is performed to ensure no duplicate results are shown
    """
    found = False
    count = 0
    med = (min_num + max_num) // 2
    for entry in _inList:
        if max_num >= min_num or not found:
            if target == entry[0]:
                found = True
            elif target > entry[0]:
                min_num = med + 1
            else:
                max_num = med - 1
        else:
            break
    return found


#This adds a cluster of CWE entries to the final list
#Each cluster is the output of a given BaseX query (after processing)
def add_cluster(_inList, prev):
    """
    This method adds a result "cluster" to the mater output list
    A cluster is the result of a given CWE sub-search
    These sub searches are done according to rank, it is assumed earlier sub-searches get higher priority
    """
    result = prev

    #If not the first cluster
    #ALGO: If not the first cluster, determine the minimum and maximum CWE
    if prev:
        #Determine the min and max numbers for the binary search
        min_num = prev[0][0]
        max_num = prev[len(prev) - 1][0]
        for entry in _inList:

            #If the ID number outside the current min-max range assume the CWE is not a duplicate
            if(int(entry[0]) < int(min_num)):
                min_num = entry[0]
                result.append(entry)
            elif(int(entry[0]) > int(max_num)):
                max_num = entry[0]
                result.append(entry)
            else:
                #ALGO: Run a binary search to check for duplicates
                if not bSearch(prev, entry[0], int(min_num), int(max_num)):
                    #Append after confirming no sucn entry already exists
                    result.append(entry)

    else:
        #If this is the first cluster, then simply return it as the output
        #(since it's impossible to have a duplicate if the query is good)
        result = _inList

    return result

def r_sort(_inList):
	"""
	This method places the search result clusters in the master list in order of rank
	Each cluster is the result of one search query
	Duplicate entries are removed (only the highest priority version remains posted)
	"""
	index = 1
        #Place the first cluster in the output automatically
	result = _inList[0]
	while(index < len(_inList)):
		if result and _inList[index]:
                        #If result and the input are valid lists...
                        #...append non-duplicate entries to the tail of the list

                        # (do NOT re-sort after appending, the order...
                        # ...of the final list needs to be preserved...
                        # ...to prioritize higher ranked queries results first)

			result = add_cluster(_inList[index], result)
		elif _inList[index]:
                        #If result is an empty list, but the next cluster is valid
                        #...there is no need to process the entry (there will be no duplicates)
			result = _inList[index]
		index += 1
	return result

#This cleans the input and gets it ready to be ran through the ranking algorithm
def process_input(_input):
    """
    This method processes the output from the search and readies to be processed through 
    the ranking algorithm
    """
    result = _input.replace("<td>", "")
    result = result.replace("\n", "")
    result = result.split("</td>")
    #Splits the result into [ID_NUM, NAME]
    #Also sorts in ascending ID_NUM order
    result = format_result_list(result)
    return result

#This converst the output into HTML table format
def process_output(rawOutput):
    result = "<table>\n"
    for entry in rawOutput:
        result += "\t<tr>\n" + "\t\t<td><a href=\"/cwe/" + entry[0] + "\">" + entry[0] + "</a></td><td><a href=\"/cwe/" + entry[0] + "\">" 
        result += entry[1] + "</a></td>\n\t</tr>\n"
    result += "</table>\n"
    return result
