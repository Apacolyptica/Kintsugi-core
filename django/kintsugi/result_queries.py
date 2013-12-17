#!/usr/bin/env python3

"""
Contains static XQuery strings for the individual CWE results pages.

START:       Start of each CWE query
RETURN:      Basic data extracted from the CWE for display
RELATION:    Relations to other CWEs
ALT_TERM:    Alternate terms referring to this CWE
"""


#All data-queries will start with an ID search
START = "declare variable $word external; "
START += " for $v in //*[@ID = $word ] return "
"""This query is the static start of any results query return"""

#This is a list of return values for the queries
#Later this list will be imported externally to promote modularity
RETURN = ["data($v/@ID) || \" \" || data($v/@Name)", \
"data($v//Description_Summary)", "data($v//Extended_Description)",]
"""
These are query-ends that produce a single output string
Enabling them to be concatenated
"""
	

#Because of stupidity in the relation data set
#Relational data needs to be handled differently
RELATION = ["data($v//Relationship_Target_Form)" \
,"data($v//Relationship_Nature)", "data($v//Relationship_Target_ID)"]
"""
These query-ends are about CWE relationships and generally produce more then one output each
This prevents concatenation and the data must be processed differently
NOTE: The database only shows relationshps 'going backward,' no 'ParentOf' relationships 
are shown from this query
"""

#TODO: Find a means to delimit and format the alt-terms
ALT_TERM = START + "data($v//Alternate_Term)"
"""
This query-end shows alternative terms of a given CWE, because it can be multiple entries
concatenating it to RETURN is impossible
"""
