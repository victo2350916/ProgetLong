from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="projet_long"
)

@app.route('/', methods={'GET'})
def index():

    return render_template('index.html')

@app.route('/ajouter')
def ajouter():

    curseur = db.cursor()

    curseur.execute("SELECT * FROM croutes")
    croutes = curseur.fetchall()

    curseur.execute("SELECT * FROM sauces")
    sauces = curseur.fetchall()

    curseur.execute("SELECT * FROM garnitures")
    garnitures = curseur.fetchall()

    return render_template('ajouter.html', croutes = croutes, sauces = sauces, garnitures = garnitures)

@app.route('/retour_commande', methods=['POST'])
def retour_commande():

    curseur = db.cursor()

    nom = request.form["nom"]
    adresse = request.form["adresse"]
    telephone = request.form["telephone"]

    sauce = request.form["sauce"]
    croute = request.form["croute"]
    garniture1 = request.form["garniture1"]
    garniture2 = request.form["garniture2"]
    garniture3 = request.form["garniture3"]
    garniture4 = request.form["garniture4"]

    curseur.execute("INSERT INTO clients(nom, numero_telephone, adresse) VALUES(%s, %s, %s)", (nom, telephone, adresse))

    curseur.execute("INSERT INTO commandes(client_id) VALUES(LAST_INSERT_ID())")

    curseur.execute("INSERT INTO pizza(commande_id, sauce_id, croute_id) VALUES(LAST_INSERT_ID(), %(sauce)s, %(croute)s)", {'sauce':sauce, 'croute':croute})

    curseur.execute("SELECT LAST_INSERT_ID()")
    pizza_id = curseur.fetchone()[0]

    curseur.execute("INSERT INTO pizza_garniture (pizza_id, garniture_id) VALUES(%(pizza_id)s, %(garniture)s)", {'pizza_id':pizza_id, 'garniture':garniture1})
    curseur.execute("INSERT INTO pizza_garniture (pizza_id, garniture_id) VALUES(%(pizza_id)s, %(garniture)s)", {'pizza_id':pizza_id, 'garniture':garniture2})
    curseur.execute("INSERT INTO pizza_garniture (pizza_id, garniture_id) VALUES(%(pizza_id)s, %(garniture)s)", {'pizza_id':pizza_id, 'garniture':garniture3})
    curseur.execute("INSERT INTO pizza_garniture (pizza_id, garniture_id) VALUES(%(pizza_id)s, %(garniture)s)", {'pizza_id':pizza_id, 'garniture':garniture4})

    curseur.execute("SELECT type FROM sauces WHERE id = %(sauce)s", {'sauce':sauce})
    sauce = curseur.fetchone()[0]

    curseur.execute("SELECT type FROM croutes WHERE id = %(croute)s", {'croute':croute})
    croute = curseur.fetchone()[0]

    curseur.execute("SELECT type FROM garnitures WHERE id = %(garniture1)s", {'garniture1':garniture1})
    garniture1 = curseur.fetchone()[0]

    curseur.execute("SELECT type FROM garnitures WHERE id = %(garniture2)s", {'garniture2':garniture2})
    garniture2 = curseur.fetchone()[0]

    curseur.execute("SELECT type FROM garnitures WHERE id = %(garniture3)s", {'garniture3':garniture3})
    garniture3 = curseur.fetchone()[0]

    curseur.execute("SELECT type FROM garnitures WHERE id = %(garniture4)s", {'garniture4':garniture4})
    garniture4 = curseur.fetchone()[0]

    db.commit()

    data = (
        nom,
        adresse,
        telephone,
        sauce,
        croute,
        garniture1,
        garniture2,
        garniture3,
        garniture4
    )

    return render_template("retour_commande.html", data = data)



@app.route('/commande_attente')
def commande_attente():

    curseur = db.cursor()

    curseur.execute("SELECT commande_attente.id, clients.nom, clients.numero_telephone, clients.adresse FROM commande_attente INNER JOIN commandes ON commandes.id = commande_attente.commande_id INNER JOIN clients ON clients.id = commandes.client_id")
    data = curseur.fetchall()

    curseur

    return render_template("commande_attente.html", data = data)

@app.route('/supprimer_commande', methods=['POST'])
def supprimer_commande():

    curseur = db.cursor()

    id = request.form["commande_id"]

    curseur.execute("DELETE FROM commande_attente WHERE commande_attente.id = %(id)s", {'id':id})

    return commande_attente()

if __name__ == '__main__':
    app.run(debug=True)