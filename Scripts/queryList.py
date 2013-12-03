# query for the string within the title
# searching within Weaknesses for a match in the element name
#         returns the ID # and the Name of the database entry with HTML table row format
nameQuery = "declare variable $word external; \
             for $v in //Weakness_Catalog/descendant-or-self::node() \
             [@Name[. contains text {$word} \
             using stemming using fuzzy ] ] \
             return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"

# query for the string located within the text
# search within the Weaknesses for a match in the element's text
#         returns the ID # and the Name of the database entry with HTML table row format
textQuery = "declare variable $word external; \
             for $v in //Weakness_Catalog/child::node()/child::node() \
             [. contains text {$word} \
             using stemming using fuzzy ]  \
             return <tr><td> { data($v//@ID) , data($v//@Name) } </td></tr>"
