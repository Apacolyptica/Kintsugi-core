# This method takes the result list and formats it to be processesd
# The input is a string that consists of a number and then some words
# Example: 919 Buffer underflow (not a real entry)
# This splits the number and name into separate elements on a list
# Because BaseX sorts numbers as a string...
# ...(for example, 94 would be "greater than" 121 with this method
# This converts the numbers to integers and sorts the list accordingly

def format_result_list(_inList):
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
    result = prev

    #If not the first cluster
    if prev:
        #Determine the min and max numbers for the binary search
        min_num = prev[0][0]
        max_num = prev[len(prev) - 1][0]
        for entry in _inList:

            #If the ID number outside the current min-max range...
            #...assume the CWE is not a duplicate
            if(int(entry[0]) < int(min_num)):
                min_num = entry[0]
                result.append(entry)
            elif(int(entry[0]) > int(max_num)):
                max_num = entry[0]
                result.append(entry)
            else:
                #Run a binary search to check for duplicates
                if not bSearch(prev, entry[0], int(min_num), int(max_num)):
                    #Append after confirming no sucn entry already exists
                    result.append(entry)

    else:
        #If this is the first cluster, then simply return it as the output
        #(since it's impossible to have a duplicate if the query is good)
        result = _inList

    return result

def r_sort(_inList):
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
        result += "\t<tr>\n" + "\t\t<td>" + entry[0] + "</td><td>" 
        result += entry[1] + "</td>\n\t</tr>\n"
    result += "</table>\n"
    return result
