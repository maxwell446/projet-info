from flask import Flask, render_template, request, flash, redirect, url_for
from python_2eme.inscription import inscription_login_orga, inscription_login_capitaine, inscription_login_arbitre, inscription_capitaine, nb_id_bdd_orga, inscription_joueur
from python_2eme.connexion import connexion_orga, connexion_arbitre, connexion_capitaine

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Ajoute une clé secrète pour utiliser flash messages

@app.route("/")
def page_html():
    return render_template('page_principale.html')
################################cote organisateur######################################

@app.route('/page_login_orga')
def page_login_orga():
    return render_template('page_login_orga.html')

@app.route('/page_incrip_orga')
def page_incrip_orga():
    return render_template('page_incrip_orga.html')



@app.route('/inscription.orga', methods=['POST'])
def inscription_orga():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        if nb_id_bdd_orga() ==0 :
            inscription_login_orga(identifiant, mdp)
            return render_template('page_login_orga.html')
    erreur="Login ou passwd impossible"
    return render_template('page_incrip_orga.html', para=erreur)


@app.route('/connexion.orga', methods=['POST'])
def connexion_organisateur():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_orga(identifiant, mdp) == True:
            return render_template('page_orga.html')
    erreur="Login ou passwd incorrect"
    return render_template('page_login_orga.html',param = erreur)

########################cote arbitre #########################
@app.route('/page_login_arbitre')
def page_login_arbitre():
    return render_template('page_login_arbitre.html')
@app.route('/page_incrip_arbitre')
def page_incrip_arbitre():
    return render_template('page_incrip_arbitre.html')


@app.route('/inscription.arbitre', methods=['POST'])
def inscription_arbitre():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login_arbitre(identifiant, mdp)
    erreur="Login ou passwd deja pris"
    return render_template('page_login_arbitre.html', para=erreur)


@app.route('/connexion.arbitre', methods=['POST'])
def connexion_arbitre2():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_arbitre(identifiant, mdp) == True:
            return render_template('page_arbitre.html')
    erreur="Login ou passwd incorrect"
    return render_template('page_login_arbitre.html',param = erreur)

################################cote capitaine##########################
@app.route('/page_login_capitaine')
def page_login_capitaine():
    return render_template('page_login_capitaine.html')

@app.route('/page_incrip_capitaine')
def page_incrip_capitaine():
    return render_template('page_incrip_capitaine.html')


@app.route('/inscription.capitaine', methods=['POST'])
def verif_inscription_capitaine():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login_capitaine(identifiant, mdp)
    erreur="Login ou passwd deja pris"
    return render_template('page_login_capitaine.html', para=erreur)

@app.route('/connexion_capitaine', methods=['POST'])
def connexion_capitaine2():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_capitaine(identifiant, mdp) == True:
            # Redirige vers la page d'inscription de l'équipe si la connexion réussit
            return redirect(url_for('inscription_equipe_form')) # Note le changement ici
    erreur="Login ou passwd incorrect"
    return render_template('page_login_capitaine.html',param = erreur)


@app.route('/form_inscription_equipe', methods=['POST'])
def gerer_inscription_equipe_joueurs():
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom_capitaine = request.form.get('nom_capitaine')
        prenom_capitaine = request.form.get('prenom_capitaine')
        nom_equipe = request.form.get('nom_equipe')
        id_equipe = inscription_capitaine(nom_capitaine, prenom_capitaine, nom_equipe)
        if id_equipe is not None:
            flash(f"L'équipe '{nom_equipe}' et le capitaine '{prenom_capitaine} {nom_capitaine}' ont été inscrits avec succès !", 'success')
            # Boucle pour récupérer et inscrire les 5 autres joueurs
            for i in range(1, 6): # Pour les joueurs 1 à 5
                prenom_joueur = request.form.get(f'prenom_player{i}')
                nom_joueur = request.form.get(f'nom_player{i}')
                success_joueur = inscription_joueur(nom_joueur, prenom_joueur, id_equipe)
                if not success_joueur:
                    flash(f"Erreur lors de l'inscription du joueur '{prenom_joueur} {nom_joueur}'.", 'warning')
            return redirect(url_for('inscription_equipe_form'))
        else:
            flash("Échec de l'inscription de l'équipe et du capitaine. Le nom d'équipe existe peut-être déjà ou une erreur interne est survenue.", 'error')
            return render_template('page_capitaine.html') 

    return redirect(url_for('page_html'))


@app.route('/page_spectateur')
def page3():
    return render_template('page_spectateur.html')

@app.route('/creer_tournoi_orga')
def page_creer_tournoi():
    return render_template('creer_tournoi_orga.html')



@app.route('/inscription_equipe_form') # Renomme la route pour être plus explicite
def inscription_equipe_form():
    return render_template('page_capitaine.html')

@app.route('/')
def afficher_formulaire_inscription():
    return render_template('page_principale.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)