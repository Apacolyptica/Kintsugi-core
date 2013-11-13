#This is a list of queries put in a separate file for easy editing 
#...and increased modularity

#I "manually" added the escape characters to the auto-generated
#...queries with filters (Q3 and 4) as well as line breaks for readability

Q1 = "declare variable $word external; for $v in \
//Weakness[. contains text {$word} using stemming \
using stop words default]return data($v/@ID)"

Q2 = "declare variable $word external; for $v in \
//Weakness[@ID[. contains text {$word} using stemming \
using stop words default]]return data($v/@ID)"

Q3 = "declare variable $word external; for $v in \
//Weakness[descendant-or-self::node()/@Language_Name = \"C++\"]\
[@Name[. contains text {$word} using stemming using stop words default]]\
return data($v/@ID)"

Q4 = "declare variable $word external; for $v in \
//Weakness[descendant-or-self::node()/\
@Language_Name = (\"C\", \"C++\", \"Java\")]\
[@Name[. contains text {$word} using stemming using stop words (\"a\")]]\
return data($v/@ID)"

NAME_QUERY = "declare variable $word external; \
for $v in //Weakness_Catalog/Weaknesses/Weakness\
[@Name[. contains text {$word} using stemming using stop words default ] ] \
return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

TEXT_QUERY = "declare variable $word external; \
for $v in //Weakness_Catalog/Weaknesses/Weakness\
[. contains text {$word} using stemming using stop words default]  \
return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

TEST_NQ = "declare variable $word external; \
for $v in //Weakness_Catalog/Weaknesses/Weakness \
[@Name[. contains text {$word} using stemming \
using stop words (\"a\",\"the\")]] \
return data($v//@ID)"

TEST_TQ = "declare variable $word external; \
for $v in //Weakness_Catalog/Weaknesses/Weakness \
[. contains text {$word} using stemming \
using stop words (\"a\",\"the\")] \
return data($v//@ID)"



# QUERY_LIST = [NAME_QUERY, TEXT_QUERY]
# QUERY_LIST = [TEST_NQ,TEST_TQ]
QUERY_LIST = [Q4]
