#!/usr/bin/env python3

"""
Generates CWE search queries.

Dynamically generates CWE search queries based on URL parameters.
"""

# All queries will start like this (maybe?)
# If we are searching for a field other than "weakness"
# ...we can dynamically add that part in

START = "declare variable $word external; for $v in //"

# All queries will end like this 
# I am only returning ID for testing purposes
# This will vary once we get our formatting in check

#Do NOT change the <td>[QUERY]</td> formatting
#The <td></td> segments are used as delimiters in later formatting methods
END = "return <td>{data($v/@ID), data($v/@Name)}</td>"

STOP_WORDS = "\"/usr/share/kintsugi/stopwords.txt\""

#fType is the type of filter (language name, OS name, etc.)
#fList is a list of one or more filters in this category
#This can potentially include ID or text...
#But we'll let the bound variable handle that
#It will be assumed the web application will allow...
#...only valid filters (it would just return blank otherwise anyway

def searchFilter(fType, fList):
	"""
	This method generates part of a query depending on the type and number of filters
	fType is a single filter to be implemented
	fList is all the filters witihn that type to be implemented
	for example (Language, [C, Java])
	this method can be evoked multiple times to add different types of filters to a query
	"""

	#Making sure fList is a list
	#All filter queries start like this
	filterStart = "[descendant-or-self::node()/@" + fType \
		+ " = "

	filters = ""
	result = ""
	
	#This is where we add the filters proper
	#The syntax depends on if we are adding one or several of them

	#ALGO: This appends the list of filters for a chosen type to the query
	if(len(fList) == 1):
		filters = "\"" + fList[0] + "\"]"
	elif(len(fList) > 1):
		filters = "(\"" + fList[0] + "\""
		place = 1
		while place < len(fList):
			filters += ", \"" + fList[place] + "\""
			place += 1

		filters += ")]"

	# Keeping the return value in one variable for ease of...
	# ...future editing

	#If there is no content then no need to add a filter list
	if(len(fList) > 0):
		result = filterStart + filters

	return result

#This is what type of search the bound variable is looking for
#This can either be name, ID, for full-text
#This will be deprecated once we include the ranking algorithm
#To prevent spirious search types (we have filters for that)...
#...The values will be "trinary" (-1, 0, or 1)
#Negative numbers represent ID search, positive represent name search
#0 represents a full text search
#Non-digits will all return 0

def searchType(sType):
	"""This dynamically generates part of a query depending on the type of search desired"""
	search = sType #Will later be error checked first

	#Without modification, this will do a full-text search
	#coreString = "[. contains text {$word} using stemming using stop words default]"
	coreString = "[. contains text {$word} using stemming using stop words at " + STOP_WORDS + " ]"
	result = coreString

	#I'll do error checking for non digits later

	if search:
		result = "[@" + sType + coreString + "]"
	
	return result

#This ties it all together and makes the query
#0 will be a placeholder value for "default settings"
#It is assumed that any filter list value will be ensured...
#...handled at the web applicaiton level

def makeQuery(field, sType, fType, fList):
	"""
	This method dynamically generates a BaseX query
	field is the field of weaknesses searched (example, 'Weakness')
	sType is the type of search being done (searching by ID, Name, etc.)
	fType is a LIST of filter categories to be appended to the query
	fList is a LIST OF LISTS of filter sub cattegories to be specified for each 'fType'
	example of filter syntax: ([Language, Operating_System_Type], [[C,C++,Java],[Windows_Vista]])
	if fType and fList are blank, enter 0 (this will be updated to accept 'False' in the future)
	"""
	
	query = START

	if not field:
		field = "Weakness"
		#Ideally the field would be a wildcard
		#but that causes strange results in the baseX full text search

	query += field

	if (fType != 0):
		#Assumes a one to one ratio between fType entries and fList lists

		fCount = 0
		while fCount < (len(fType)):
			query += searchFilter(fType[fCount], fList[fCount])
			fCount += 1

	query += searchType(sType)
	query += END

	return query
