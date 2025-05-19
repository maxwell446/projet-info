from flask import Flask, render_template, request
from python_2eme.inscription import inscription_login_orga, inscription_login_capitaine, inscription_login_arbitre
from python_2eme.connexion import connexion_orga, connexion_arbitre, connexion_capitaine

app = Flask(__name__)


@app.route("/")
def page_html():
    return render_template("page_principale.html")

@app.route('/page_login_arbitre.html')
def page_login_arbitre():
    return render_template('page_login_arbitre.html')

@app.route('/page_login_capitaine.html')
def page_login_capitaine():
    return render_template('page_login_capitaine.html')

@app.route('/page_login_orga.html')
def page_login_orga():
    return render_template('page_login_orga.html')

@app.route('/page_incrip_arbitre.html')
def page_incrip_arbitre():
    return render_template('page_incrip_arbitre.html')

@app.route('/page_incrip_capitaine.html')
def page_incrip_capitaine():
    return render_template('page_incrip_capitaine.html')

@app.route('/page_incrip_orga.html')
def page_incrip_orga():
    return render_template('page_incrip_orga.html')

@app.route('/page_spectateur.html')
def page3():
    return render_template('page_spectateur.html')

@app.route('/creer_tournoi.html')
def page_creer_tournoi():
    return render_template('creer_tournoi.html')




@app.route('/inscription.orga', methods=['POST'])
def inscription_orga():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login_orga(identifiant, mdp)
    erreur="Login ou passwd deja pris"
    return render_template('page_login_orga.html', para=erreur)

@app.route('/inscription.arbitre', methods=['POST'])
def inscription_arbitre():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login_arbitre(identifiant, mdp)
    erreur="Login ou passwd deja pris"
    return render_template('page_login_arbitre.html', para=erreur)

@app.route('/inscription.capitaine', methods=['POST'])
def inscription_capitaine():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login_capitaine(identifiant, mdp)
    erreur="Login ou passwd deja pris"
    return render_template('page_login_capitaine.html', para=erreur)


@app.route('/connexion.orga', methods=['POST'])
def connexion_organisateur():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_orga(identifiant, mdp) == True:
            return render_template('page_orga.html')
    erreur="Login ou passwd incorrect"
    return render_template('page_login_orga.html',param = erreur)

@app.route('/connexion.arbitre', methods=['POST'])
def connexion_arbitre2():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_arbitre(identifiant, mdp) == True:
            return render_template('page_arbitre.html')
    erreur="Login ou passwd incorrect"
    return render_template('page_login_arbitre.html',param = erreur)
""""""
@app.route('/connexion.capitaine', methods=['POST'])
def connexion_capitaine2():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_capitaine(identifiant, mdp) == True:
            return render_template('page_capitaine.html')
    erreur="Login ou passwd incorrect"
    return render_template('page_login_capitaine.html',param = erreur)
""""""

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


@app.route('/inscription.joueur', methods=['POST'])
def inscription_joueur():
    if request.method == 'POST':
        nom_capitaine = request.form['nom_capitaine']
        prenom_capitaine = request.form['prenom_capitaine']
        nom_equipe = request.form['nom_equipe']
        inscription_capitaine(nom_capitaine,prenom_capitaine,nom_equipe)
    return render_template('page_principale.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')

