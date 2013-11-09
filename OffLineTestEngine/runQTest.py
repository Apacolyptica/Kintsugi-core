#!/usr/local/bin/python3

#import BaseXClient
import qtest
import sys
from qList import QUERY_LIST

#session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

#session.execute("open cwec_v2-5")

#sys.exit(0)

#NAME_QUERY = "declare variable $word external; \
#for $v in //Weakness_Catalog/Weaknesses/Weakness[@Name[. contains text {$word} ] ] \
#return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

#TEXT_QUERY = "declare variable $word external; \
#for $v in //Weakness_Catalog/Weaknesses/Weakness[. contains text {$word} ]  \
#return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

#This is using external arguments in place of web-forms

if (len(sys.argv) < 2):
	print("Usage " + sys.argv[0] + " search-term")
	print("Example: " + sys.argv[0] + " buffer")

else:
	# Adds a variable number of queries from an external file
	searches = []
	for query in QUERY_LIST:
		searches.append(qtest.dbSearch(sys.argv[1], query))

	# searches = [str(qtest.dbSearch(sys.argv[1], NAME_QUERY)), \ 
	# str(qtest.dbSearch(sys.argv[1], TEXT_QUERY))]

	print(qtest.output(searches))
	# print("End")
