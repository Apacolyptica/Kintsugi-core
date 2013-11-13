# All queries will start like this (maybe?)
START = "declare variable $word external; for $v in //Weakness"

# All queries will end like this 
# I am only returning ID for testing purposes
# This will vary once we get our formatting in check

END = "return data($v/@ID)"
# END = "return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

#fType is the type of filter (language name, OS name, etc.)
#fList is a list of one or more filters in this category
#This can potentially include ID or text...
#But we'll let the bound variable handle that
#It will be assumed the web application will allow...
#...only valid filters (it would just return blank otherwise anyway

def searchFilter(fType, fList):

	#Making sure fList is a list
	#All filter queries start like this
	filterStart = "[descendant-or-self::node()/@" + fType \
		+ " = "

	filters = ""
	result = ""
	
	#This is where we add the filters proper
	#The syntax depends on if we are adding one or several of them

	if(len(fList) == 1):
		filters = "\"" + fList[0] + "\"]"
	elif(len(fList) > 1):
		filters = "(\"" + fList[0] + "\""
		place = 1
		while place < len(fList):
			filters += ", \"" + fList[place] + "\""
			place += 1
			#Why the **** does python not have a...
			#..."++" function?

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
	search = sType #Will later be error checked first

	#Without modification, this will do a full-text search
	coreString = "[. contains text {$word} using stemming using stop words default]"
	result = coreString

	#I'll do error checking for non digits later

	#Could automate this part to one sub-method to cut down on redundant code
	if(search < 0):
		result = "[@ID" + coreString + "]"
	elif(search > 0):
		result = "[@Name" + coreString + "]"
	
	return result

#This ties it all together and makes the query
#0 will be a placeholder value for "default settings"
#It is assumed that any filter list value will be ensured...
#...handled at the web applicaiton level

def makeQuery(sType, fType, fList):
	query = START

	#if there are no filters, fType will be 0
	if (fType != 0):
		query += searchFilter(fType, fList)

	query += searchType(sType)
	query += END

	return query
