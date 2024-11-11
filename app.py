from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="votre_user",
    passwd="votre_mot_de_passe",
    database="nom_de_la_base_de_donnees"
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM votre_table")
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)