import csv
import pandas as pd
import json
import os
import bcrypt
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = os.urandom(24)


# define a function to check if a password matches a hash
def check_password(result, password):
    # use bcrypt to check if the password matches the hash
    if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
        return True
    else:
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the user's input (e.g. from a form)
        username = request.form['username']
        password = request.form['password']

        # connect to the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # retrieve the user's record from the database
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        result = c.fetchone()

        # close the database connection
        conn.close()

        if check_password(result, password):
            # log the user in and set session variables
            session['user_id'] = result[0]
            session['username'] = username

            return redirect(url_for('home'))

        else:
            # display an error message
            flash('Invalid login')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route("/")
def home():
    """
    Renvoie la page d'accueil (index.html).
    """
    user_id = session.get('user_id')
    username = session.get('username')
    if user_id is None:
        return redirect(url_for('login'))
    return render_template("index.html")


@app.route("/ajout")
def ajout():
    """
    Renvoie la page pour ajouter un nouveau parc (ajout.html).
    """
    # Vérifier si l'utilisateur est connecté
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    return render_template("ajout.html")


@app.route("/modification")
def modification():
    """
    Renvoie la page pour modifier les informations d'un parc (modification.html).
    Charge également les données du fichier CSV dans un dictionnaire et renvoie
    une liste JSON pour être utilisée dans le formulaire.
    """
    # Vérifier si l'utilisateur est connecté
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    # Ouvrir le fichier CSV et lire les données
    df = pd.read_csv("data.csv", delimiter=';', encoding="windows-1252")
    options = list(df['nomParc'].unique())
    jsonfiles = json.loads(df.to_json(orient='records'))
    return render_template("modification.html", options=options, df=jsonfiles)


@app.route("/add", methods=["POST"])
def add():
    """
    Ajoute les données du formulaire dans le fichier CSV.
    Renvoie un message de confirmation.
    """
    # Vérifier si l'utilisateur est connecté
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    # Get the uploaded file from the form data
    geojson_file = request.files['geometry']

    # Check if the geometry file is empty
    if geojson_file.filename == '':
        geojson_data = {'type': 'FeatureCollection', 'features': []}
    else:
        # Read the contents of the file
        dataGeojson = geojson_file.read()

        # Convert the file content to a JSON object
        geojson_data = json.loads(dataGeojson)

    # Extract the geometries from the JSON object
    features = geojson_data['features']
    geometries = [feature['geometry'] for feature in features]

    # Récupérer les données du formulaire
    data = [
        request.form.get('nomParc'),
        request.form.get('typeParc'),
        request.form.get('superficie'),
        request.form.get('dateCreation'),
        request.form.get('arrondissement'),
        request.form.get('dateOfficialisation'),
        request.form.get('Amenagement_1'),
        request.form.get('Amenagement_2'),
        request.form.get('Amenagement_3'),
        request.form.get('Amenagement_4'),
        request.form.get('Amenagement_5'),
        request.form.get('Amenagement_6'),
        request.form.get('Amenagement_7'),
        request.form.get('Amenagement_8'),
        request.form.get('Amenagement_9'),
        request.form.get('Amenagement_10'),
        geometries[0],
        request.form.get('nom'),
        request.form.get('dateNaissance'),
        request.form.get('dateDeces'),
        request.form.get('profession'),
        request.form.get('employeur'),
        request.form.get('lieuEtudes'),
        request.form.get('nbreEnfants')
    ]
    # Écrire les données dans le fichier CSV
    with open("data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        # Écrire l'en-tête s'il n'y a pas de données dans le fichier
        if csvfile.tell() == 0:
            header = [
                'nomParc',
                'typeParc',
                'superficie',
                'dateCreation',
                'arrondissement',
                'dateOfficialisation',
                'Amenagement_1',
                'Amenagement_2',
                'Amenagement_3',
                'Amenagement_4',
                'Amenagement_5',
                'Amenagement_6',
                'Amenagement_7',
                'Amenagement_8',
                'Amenagement_9',
                'Amenagement_10',
                'geometry',
                'nom',
                'dateNaissance',
                'dateDeces',
                'profession',
                'employeur',
                'lieuEtudes',
                'nbreEnfants'
            ]
            writer.writerow(header)
        # Écrire les données du formulaire dans une nouvelle ligne
        writer.writerow(data)
    return "Nouveau parc ajouté avec succès !"


@app.route("/update", methods=["POST"])
def update():
    """
    Modifie les données d'un parc dans le fichier CSV en utilisant les données
    du formulaire. Renvoie un message de confirmation.
    """
    # Vérifier si l'utilisateur est connecté
    if 'username' not in session:
        return redirect(url_for('login'))


    # Récupérer les données du formulaire
    nomParc = request.form.get('nomParc')
    typeParc = request.form.get('typeParc')
    superficie = request.form.get('superficie')
    dateCreation = request.form.get('dateCreation')
    arrondissement = request.form.get('arrondissement')
    dateOfficialisation = request.form.get('dateOfficialisation')
    Amenagement_1 = request.form.get('Amenagement_1')
    Amenagement_2 = request.form.get('Amenagement_2')
    Amenagement_3 = request.form.get('Amenagement_3')
    Amenagement_4 = request.form.get('Amenagement_4')
    Amenagement_5 = request.form.get('Amenagement_5')
    Amenagement_6 = request.form.get('Amenagement_6')
    Amenagement_7 = request.form.get('Amenagement_7')
    Amenagement_8 = request.form.get('Amenagement_8')
    Amenagement_9 = request.form.get('Amenagement_9')
    Amenagement_10 = request.form.get('Amenagement_10')

    # Get the uploaded file from the form data
    geojson_file = request.files['geometry']

    # Check if the geometry file is empty
    if geojson_file.filename == '':
        geojson_data = {'type': 'FeatureCollection', 'features': []}
    else:
        # Read the contents of the file
        dataGeojson = geojson_file.read()

        # Convert the file content to a JSON object
        geojson_data = json.loads(dataGeojson)

    # Extract the geometries from the JSON object
    features = geojson_data['features']
    geometries = [feature['geometry'] for feature in features]

    nom = request.form.get('nom')
    dateNaissance = request.form.get('dateNaissance')
    dateDeces = request.form.get('dateDeces')
    profession = request.form.get('profession')
    employeur = request.form.get('employeur')
    lieuEtudes = request.form.get('lieuEtudes')
    nbreEnfants = request.form.get('nbreEnfants')
    # Charger les données CSV dans un dictionnaire + on prend une liste rows
    data = {}
    rows = []
    with open("data.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        # Lire les en-têtes des colonnes
        header = reader.fieldnames
        for row in reader:
            # On définit notre clé de recherche comme "nomParc" et on parcourt les lignes une à une
            key = row["nomParc"]
            data[key] = row
            # S'il existe déjà le nom du parc dans le CSV, on modifie les infos avec ce qui vient du formulaire puis on
            # ajoute la ligne à la liste
            if key == nomParc:
                row["typeParc"] = typeParc
                row["superficie"] = superficie
                row["dateCreation"] = dateCreation
                row["arrondissement"] = arrondissement
                row["dateOfficialisation"] = dateOfficialisation
                row["Amenagement_1"] = Amenagement_1
                row["Amenagement_2"] = Amenagement_2
                row["Amenagement_3"] = Amenagement_3
                row["Amenagement_4"] = Amenagement_4
                row["Amenagement_5"] = Amenagement_5
                row["Amenagement_6"] = Amenagement_6
                row["Amenagement_7"] = Amenagement_7
                row["Amenagement_8"] = Amenagement_8
                row["Amenagement_9"] = Amenagement_9
                row["Amenagement_10"] = Amenagement_10
                row["geometry"] = geometries
                row["nom"] = nom
                row["dateNaissance"] = dateNaissance
                row["dateDeces"] = dateDeces
                row["profession"] = profession
                row["employeur"] = employeur
                row["lieuEtudes"] = lieuEtudes
                row["nbreEnfants"] = nbreEnfants
                rows.append(row)
            # Sinon on ajoute la ligne à la liste tel quel pour conserver les autres infos
            else:
                rows.append(row)
    # Écrire les lignes mises à jour dans un nouveau fichier CSV
    with open("data.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=header)
        # Écrire les en-têtes des colonnes
        writer.writeheader()
        # # Écrire les nouvelles lignes dans le fichier
        writer.writerows(rows)
    return "Données de parc modifiées avec succès !"


if __name__ == "__main__":
    app.run(debug=True)


