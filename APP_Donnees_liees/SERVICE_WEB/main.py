# coding=utf-8

"""
Projet de session - Service de données web
Réalisé par Benoit Campeau, Daphnée D'Amour
Présenté à M. Yves Voirin
Pour le cours GMQ580 - GéoInformatique II
avril 2023
"""

# ================================================================================================
# LIBRARY
from flask import Flask, request, render_template
from requests import post

# ================================================================================================
# GLOBALS VARIABLES
# SPARQL query template to retrieve parc data from Fuseki
QUERY_TEMPLATE_PARC = """
    prefix geo:   <http://www.opengis.net/ont/geosparql#> 
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix crs:   <http://www.opengis.net/def/crs/EPSG/0/> 
    prefix xsd:   <http://www.w3.org/2001/XMLSchema#> 
    prefix gev:   <https://[servername]/~gev/> 
    prefix crmgeo: <http://www.cidoc-crm.org/rdfs/1.0/crmgeo#> 
    prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> 
    prefix crm:   <http://www.cidoc-crm.org/cidoc-crm/> 
  
    SELECT ?name ?feature ?init_area ?currentnamedate ?geomGeoJSON
	WHERE { ?x gev:name ?name .
      		?x ?a crm:E53_Place .
  			?x gev:feature ?feature .
      		?x gev:init_area ?init_area .
  			?x gev:currentnamedate ?currentnamedate .
  			?geom crmgeo:Q11_approximates ?x .
  			?geom geo:asGeoJSON ?geomGeoJSON
  			%s }
   """

# SPARQL query template to retrieve person data from Fuseki
QUERY_TEMPLATE_PERSON = """
    prefix geo:   <http://www.opengis.net/ont/geosparql#>
	prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	prefix gev:   <http://[servername]/~gev/>
	
    SELECT ?name
	WHERE { ?x gev:name ?name .
	%s }
	""" # A FAIRE

# SPARQL query template to retrieve viewpoint data from Fuseki
QUERY_TEMPLATE_VIEWPOINT = """ 
    prefix geo:   <http://www.opengis.net/ont/geosparql#>
	prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	prefix gev:   <http://[servername]/~gev/>
	
    SELECT ?name
	WHERE { ?x gev:name ?name .
	%s }
	""" # A FAIRE

# SPARQL query template to retrieve aerial photography data from Fuseki
QUERY_TEMPLATE_PHOTO = """ 
    prefix geo:   <http://www.opengis.net/ont/geosparql#>
	prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	prefix gev:   <http://[servername]/~gev/>
	
    SELECT ?name
	WHERE { ?x gev:name ?name .
	%s }
	""" # A FAIRE

# SPARQL filters for query {<arg name>: <SPARQL filter>}
FILTERS = { "year": "?currentnamedate < %s",
            "name": "?name = %s" }

# JSON template for 1 feature
FEATURE_TEMPLATE = { "type": "Feature",
                     "properties": {} ,
                     "geometry": {} }

# GeoJSON template for 1 Feature Collection
GEOJSON_TEMPLATE = { "type": "FeatureCollection",
                     "crs": { "type": "name",
                              "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
                     "features": [] }

DATASET = 'test_service_web' # Fuseki dataset name
DEFAULT_CRS = "urn:ogc:def:crs:EPSG::3758" # The default crs for geometric data is EPSG:3758
# ================================================================================================
# FUNCTIONS
def FusekiQuery(query, datasetname):
    """
    FusekiQuery(query, dataset) -> new POST request
    Send SPARQL query to Fuseki with POST request and return the response to JSON-LD format (dict)

    Keyword arguments
        query : SPARQL query to send
        datasetname : name of the dataset to query

    Apache Jena Fuseki REST documentation : https://jena.apache.org/documentation/fuseki2/soh.html
    """

    # The endpoint include de dataset name ('%s')
    response = post("http://[servername]/%s/query" % datasetname,  # Fuseki REST query endpoint
                    headers={'Accept': 'application/sparql-results+json'},  # response format
                    data={'query': query})  # SELECT SPARQL query

    # Check request status
    if response.status_code == 200:
        print('RDF data received successfully')
    else:
        print('Failed to send query')
        print(response.content)

    # Return response in JSON-LD format (dict)
    return response.json()

# ================================================================================================
# FLASK SERVICE
app = Flask(__name__)

# html template map
@app.route("/")
def gabarit_map():
    """
    http//:<servername>:<port> -> load interactive map form templates
    """
    return render_template('index.html')

@app.route('/map/')
@app.route('/map/<datatype>/')
def map(datatype='parc'):
    """
    http//:<servername>:<port>/map/<datatype> -> call web service

    Data web service that retrieve RDF data from Apache Jena Fuseki
    and convert geometric data to GeoJSON (dict)

        /map -> return PARC data to GeoJSON (dict)
            ?name -> apply filter on parc name (= ?name)
            ?year -> apply filter on parc currentnamedate (< ?year)
            ...
        /map/person -> return PERSON data to JSON-LD (dict)
            ...
        /map/viewpoint -> return VIEWPOINT data to GeoJSON (dict)
            ...
        /map/photo -> return aerial PHOTO data to JSON-LD (dict)

    """

    # Input argument in query
    filter_query = []
    for arg in FILTERS:
        # Extract arguments value from the get request
        arg_value = request.args.get(arg)
        # Construct filter SPARQL query
        if arg_value is not None:
            if arg_value.isdigit() or arg_value.isdecimal():
                filter_query.append( "FILTER ( %s )" % (FILTERS[arg] % arg_value) )
            else:
                filter_query.append( "FILTER ( %s )" % (FILTERS[arg] % ('"' + arg_value + '"')) )

    # Insert the filter in template for SPARQL query
    if datatype == "person":
        query = QUERY_TEMPLATE_PERSON % ' '.join(filter_query)
    elif datatype == "viewpoint" :
        query = QUERY_TEMPLATE_VIEWPOINT % ' '.join(filter_query)
    elif datatype == "photo" :
        query = QUERY_TEMPLATE_PHOTO % ' '.join(filter_query)
    else:
        query = QUERY_TEMPLATE_PARC % ' '.join(filter_query)

    print('Sending SPARQL query to Apache Jena Fuseki : ')
    print(query)

    # Send SPARQL query with POST request
    query_result = FusekiQuery(query, DATASET)
    #print(query_result)
    #print(FusekiQuery.__doc__)
    #print(query_result.__doc__)

    if datatype in ("person", "photo"):
        return query_result # return query response

    else:
        # Extract query response information
        features_list = []
        # Parse feature
        for feature in query_result['results']['bindings']:
            geometry = {}
            properties = {}
            # Initiate feature dict form template
            feature_json = FEATURE_TEMPLATE.copy()
            # Parse feature element
            for key in feature:
                if key == 'geomGeoJSON':
                    # Extract geometry
                    geometry = eval(feature[key]['value'])
                else:
                    # Check if properties are integer
                    if feature[key]['value'].isdigit():
                        # Extract feature properties and cast them to integer
                        properties[key] = int(feature[key]['value'])
                    else:
                        # Extract feature properties
                        properties[key] = feature[key]['value']

            # Insert feature information to dict
            feature_json['properties'] = properties
            feature_json['geometry'] = geometry

            # Insert features to list
            features_list.append(feature_json)

        # Initiate collection dict form template
        collection_json = GEOJSON_TEMPLATE.copy()
        # Insert crs and feature list to collection dict
        collection_json['crs']['properties']['name'] = DEFAULT_CRS
        if len(features_list) > 0:
            collection_json['features'] = features_list

        return collection_json # Return collection dict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556, debug=True)
    #app.run(debug=True)