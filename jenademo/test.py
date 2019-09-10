
from jenademo.jena_spqrql_endpoint import *

entities = ["失眠"]

SPARQL_PREXIX = "PREFIX ldt: <http://www.kg.org/>\n" \
                "PREFIX ns1: <ldt:>\n" \
                "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"

SPARQL_SELECT_TEM = "{prefix}" \
                    "SELECT ?s ?o \n" \
                    "WHERE {{ \n" \
                    "\t{expression}" \
                    "}}\n"

for entity in entities:
    e = "?s rdf:type ns1:Disease .\n\t" \
        "?s ns1:acompany_with ?o .\n\t" \
        "?o ns1:disease_name '{entity}' .\n".format(entity=entity)

    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, expression=e)
    print(sparql)
    fuseki = JenaFuseki()
    result = fuseki.get_sparql_result(sparql)
    pass