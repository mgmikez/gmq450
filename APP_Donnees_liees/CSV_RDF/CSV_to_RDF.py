import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, FOAF  # importations des librairies courantes
from requests import post

# Define namespaces for RDF terms
GEV = Namespace("https://www.geoespacesverts.com/")

# Load data from CSV file
df = pd.read_csv('../FORMULAIRE/data.csv',
                 delimiter=";",
                 keep_default_na=False,
                 encoding="windows-1252")

# Variable pour les cellules vides
empty = ""

# Create an RDF graph
graph = Graph()
graph.bind("foaf", FOAF)
graph.bind("gev", GEV)

# Add triples to the graph
for index, row in df.iterrows():

    # Create subject URI
    subject = URIRef(f"{GEV}{row['nom']}".replace(" ", ""))
    # A ajouter : un attribut pour savoir si le parc est nommé après une personne / évènement / etc
    # Add property triples avec check des cellules vides
    graph.add((subject, RDF.type, FOAF.Person))
    if row['nom'] is not empty: graph.add((subject, FOAF.name, Literal(row['nom'])))
    if row['dateNaissance'] is not empty: graph.add((subject, FOAF.birthday, Literal(row['dateNaissance'])))
    if row['dateDeces'] is not empty: graph.add((subject, GEV.deathdate, Literal(row['dateDeces'])))
    if row['profession'] is not empty: graph.add((subject, FOAF.currentProject, Literal(row['profession'])))
    if row['employeur'] is not empty: graph.add((subject, GEV.employer, Literal(row['employeur'])))
    if row['lieuEtudes'] is not empty: graph.add((subject, GEV.school, Literal(row['lieuEtudes'])))
    if row['nbreEnfants'] is not empty: graph.add((subject, GEV.nbchildren, Literal(row['nbreEnfants'])))
    graph.add((subject, RDF.type, GEV.Parc))
    if row['nomParc'] is not empty: graph.add((subject, GEV.name, Literal(row['nomParc'])))
    if row['typeParc'] is not empty: graph.add((subject, GEV.type, Literal(row['typeParc'])))
    if row['superficie'] is not empty: graph.add((subject, GEV.init_area, Literal(row['superficie'])))
    if row['dateCreation'] is not empty: graph.add((subject, GEV.creationdate, Literal(row['dateCreation'])))
    if row['arrondissement'] is not empty: graph.add((subject, GEV.district, URIRef(f"{GEV}{row['arrondissement']}".replace(" ", ""))))
    if row['dateOfficialisation'] is not empty: graph.add((subject, GEV.officialisation, Literal(row['dateOfficialisation'])))
    if row['nbreAmenagements'] is not empty: graph.add((subject, GEV.nbfeatures, Literal(row['nbreAmenagements'])))


### SUPPRIMER LES DONNEES EXISTANTES
# Requete SPARQL pour la suppression des données
drop = """
    DROP ALL
"""
# On envoie ça par une requête post à Apache Jena
response = post('https://[servername]/update', data={'update': drop})

# On vérifie la réponse
if response.status_code == 200:
    print('RDF data remove successfully')
else:
    print('Failed to remove RDF data')
    print(response.content)

## AJOUTER LES NOUVELLES DONNEES
# Requete SPARQL pour parcourir le graph et insérer les données
update = """
    INSERT DATA {
            %s
    }
""" % graph.serialize(format='nt')  # 'nt' -> tel quel

# On envoie ça par une requête post à Apache Jena
response = post('https://[servername]/update', data={'update': update})

# On vérifie la réponse
if response.status_code == 200:
    print('RDF data added successfully')
else:
    print('Failed to add RDF data')
    print(response.content)

# On se crée un fichier de sortie en xml (peut servir de backup)
graph.serialize(destination='output.rdf', format='xml')

# Affichage des triplets dans la console
for triple in graph:
    print(triple)

