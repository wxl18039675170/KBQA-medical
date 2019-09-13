# KBQA-medical

Before starting, you need to download apache-jena-3.12.0 and apache-jena-fuseki-3.12.0. put the two libs to our project root.
#1. Download raw data

    1. spider data xunyiwenyao portal
        python ./crawler/xywy_spider.py
    2. export data from MongoDB
        mongoexport -h localhost:27017 -d xywy -c jib -o "/Users/allen/PycharmProjects/KBQA-medical/data/medical.json"
        

#2. Clean raw data to RDF

    1. build rdf iri
        python ./medical_rdf_IRI_id.py 
    2. build rdf
        python ./build_medical_rdf.py
        
#3. Load data to neo4j server
    3. build neo4j graph
        python ./build_medical_graph.py
        
#4. Load data to jena TDB

    1. cd ./apache-jena-3.12.0/bin
    2. ./tdbloader -o "/Users/allen/PycharmProjects/KBQA-medical/apache-jena-fuseki-3.12.0/tdb" "/Users/allen/PycharmProjects/KBQA-medical/data/medical.ttl"
    3. cd  ./Users/allen/PycharmProjects/KBQA-medical/apache-jena-fuseki-3.12.0
    4. ./fuseki-server   and stop fuseki-server
    5. put "/Users/allen/PycharmProjects/KBQA-medical/data/fuseki_conf.ttl" to "/Users/allen/PycharmProjects/KBQA-medical/apache-jena-fuseki-3.12.0/run/configuration"
       put "/Users/allen/PycharmProjects/KBQA-medical/data/ontology.ttl" to "/Users/allen/PycharmProjects/KBQA-medical/apache-jena-fuseki-3.12.0/run/databases"
    6. restart server  ./fuseki-server
    

#5. start chatbot(OWL-base)

    1. cd "/Users/allen/PycharmProjects/KBQA-medical/jenademo"
    2. python ./kbqa_main.py
    
    
#6. start chatbot(Neo4j-base)
    Note: you need to start neo4j server
    1. cd "/Users/allen/PycharmProjects/KBQA-medical/neo4jdemo"
    2. python chatbot_graph
    
        

