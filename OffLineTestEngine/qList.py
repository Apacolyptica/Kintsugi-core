#This is a list of queries put in a separate file for easy editing and increased modularity



NAME_QUERY = "declare variable $word external; \
for $v in //Weakness_Catalog/Weaknesses/Weakness\
[@Name[. contains text {$word} using stemming using stop words default ] ] \
return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

TEXT_QUERY = "declare variable $word external; \
for $v in //Weakness_Catalog/Weaknesses/Weakness\
[. contains text {$word} using stemming using stop words default]  \
return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

QUERY_LIST = [NAME_QUERY, TEXT_QUERY]
