from flask import Flask, render_template, request
from python_2eme.connexion import connexion1
from python_2eme.inscription import inscription_login

app = Flask(__name__)

@app.route("/")
def page_html():
    return render_template("index.html")

@app.route("/traitement", methods=["POST"])
def traitement():
    print("Formulaire reçu !")
    nom_utilisateur = request.form.get("nom") # Récupération de la donnée envoyée
    mot_de_passe = request.form.get("mdp")
    inscription_login(nom_utilisateur, mot_de_passe)
    return f"<h2>Bonjour, {nom_utilisateur} !</h2>"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)







@app.route('/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login(identifiant, mdp)
    return render_template('page_incrip.html')
