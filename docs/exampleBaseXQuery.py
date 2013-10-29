# Example query script for BaseX
# Opens the CWE database, queries for a particular node, prints the WHOLE node,
#      and exits.

import BaseXClient
from KintsugiSettings import BASEX_KINTSUGI_PASSWORD

# Create session
session = BaseXClient.Session('localhost', 1984, 'kintsugi', BASEX_KINTSUGI_PASSWORD)

try:
    # Open the CWE database
    session.execute("open cwec_v2-5")

    # Create query, with placeholder for the parameter
    queryText = "declare variable $id external; \
                 for $v in //Weakness_Catalog/Views/View[@ID = $id] \
                 return $v"

    # Send the query
    query = session.query(queryText)

    # Bind the parameter
    query.bind("$id", "1000")

    # Execute query and print result
    print(query.execute())

    # Close query object
    query.close()

finally:
    # Close session
    if session:
        session.close()
