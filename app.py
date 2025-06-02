from flask import Flask, render_template, request, flash, redirect, url_for
from python_2eme.inscription import inscription_login_orga, inscription_login_capitaine, inscription_login_arbitre, inscription_capitaine, nb_id_bdd_orga
from python_2eme.connexion import connexion_orga, connexion_arbitre, connexion_capitaine

app = Flask(__name__)


@app.route("/")
def page_html():
    return render_template('page_principale.html')

@app.route('/page_login_arbitre')
def page_login_arbitre():
    return render_template('page_login_arbitre.html')

@app.route('/page_login_capitaine')
def page_login_capitaine():
    return render_template('page_login_capitaine.html')

@app.route('/page_login_orga')
def page_login_orga():
    return render_template('page_login_orga.html')

@app.route('/page_incrip_arbitre')
def page_incrip_arbitre():
    return render_template('page_incrip_arbitre.html')

@app.route('/page_incrip_capitaine')
def page_incrip_capitaine():
    return render_template('page_incrip_capitaine.html')

@app.route('/page_incrip_orga')
def page_incrip_orga():
    return render_template('page_incrip_orga.html')

@app.route('/page_spectateur')
def page3():
    return render_template('page_spectateur.html')

@app.route('/creer_tournoi_orga')
def page_creer_tournoi():
    return render_template('creer_tournoi_orga.html')




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

@app.route('/connexion_capitaine', methods=['POST'])
def connexion_capitaine2():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_capitaine(identifiant, mdp) == True:
            return render_template('page_capitaine.html')
    erreur="Login ou passwd incorrect"
    return render_template('page_login_capitaine.html',param = erreur)

@app.route('/')
def afficher_formulaire_inscription():
    return render_template('page_principale.html') 
"""""
@app.route('/inscription.joueur', methods=['POST'])
def inscription_joueur():
    if request.method == 'POST':
        nom_capitaine = request.form.get('nom_capitaine')
        prenom_capitaine = request.form.get('prenom_capitaine')
        nom_equipe = request.form.get('nom_equipe')
        inscription_capitaine(nom_capitaine,prenom_capitaine,nom_equipe)
        
    id_equipe = inscription_capitaine(nom_capitaine, prenom_capitaine, nom_equipe)
        
    if id_equipe is not None:
        for i in range(1, 6):
            prenom_joueur = request.form.get(f'prenom_player{i}')
            nom_joueur = request.form.get(f'nom_player{i}')
            if prenom_joueur and nom_joueur: 
                success_joueur = inscription_joueur(nom_joueur, prenom_joueur, id_equipe)
                if not success_joueur:
                    flash(f"Erreur lors de l'inscription du joueur '{prenom_joueur} {nom_joueur}'.", 'warning')
                elif prenom_joueur or nom_joueur: 
                    flash(f"Veuillez fournir le nom ET le prénom pour le joueur {i} afin de l'inscrire.", 'info')

         
            return redirect(url_for('afficher_formulaire_inscription'))
        else:
            flash("Échec de l'inscription de l'équipe et du capitaine. Le nom d'équipe existe peut-être déjà ou une erreur est survenue.", 'error')
            return render_template('page_principale.html')
    return redirect(url_for('afficher_formulaire_inscription'))

"""""
@app.route('/inscription.joueur', methods=['POST'])
def gerer_inscription_equipe_joueurs(): 
    if request.method == 'POST':
        # Récupération des données du capitaine et de l'équipe
        nom_capitaine = request.form.get('nom_capitaine')
        prenom_capitaine = request.form.get('prenom_capitaine')
        nom_equipe = request.form.get('nom_equipe')

        # 1. Inscription du capitaine et de l'équipe dans la base de données
        # APPEL UNIQUE et CAPTURE du résultat
        id_equipe = inscription_capitaine(nom_capitaine, prenom_capitaine, nom_equipe)
        
        # Vérification si l'inscription du capitaine et de l'équipe a réussi
        if id_equipe is not None:
            flash(f"L'équipe '{nom_equipe}' et le capitaine '{prenom_capitaine} {nom_capitaine}' ont été inscrits avec succès !", 'success')

            # 2. Inscription des autres joueurs de l'équipe (s'ils sont renseignés)
            # Boucle pour récupérer et inscrire les 5 autres joueurs
            for i in range(1, 6): # Pour les joueurs 1 à 5
                prenom_joueur = request.form.get(f'prenom_player{i}')
                nom_joueur = request.form.get(f'nom_player{i}')

                # Inscrit le joueur seulement si le prénom ET le nom sont fournis
                if prenom_joueur and nom_joueur:
                    success_joueur = inscription_joueur(nom_joueur, prenom_joueur, id_equipe)
                    if not success_joueur:
                        flash(f"Erreur lors de l'inscription du joueur '{prenom_joueur} {nom_joueur}'.", 'warning')
                # Condition pour le cas où un seul champ est rempli pour un joueur donné (optionnel)
                elif prenom_joueur or nom_joueur: 
                    flash(f"Veuillez fournir le nom ET le prénom pour le joueur {i} afin de l'inscrire.", 'info')
            
            # --- Le REDIRECT se fait ICI, APRÈS la boucle et tout le traitement ---
            return redirect(url_for('afficher_formulaire_inscription'))
            # ---------------------------------------------------------------------

        else:
            # Si l'inscription du capitaine/équipe a échoué (par exemple, nom d'équipe déjà pris)
            flash("Échec de l'inscription de l'équipe et du capitaine. Le nom d'équipe existe peut-être déjà ou une erreur interne est survenue.", 'error')
            # On re-rend la page avec le formulaire pour que l'utilisateur puisse voir le message d'erreur
            return render_template('page_principale.html')
            
    # Ce return est un repli au cas où la requête ne serait pas POST (ce qui ne devrait pas arriver ici)
    return redirect(url_for('afficher_formulaire_inscription'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)