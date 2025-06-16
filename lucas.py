from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import sqlite3

from python_lucas.inscription import get_all_team_names, ajouter_score, generer_calendrier_round_robin, get_db_connection, get_nb_equipe_in_competition, inscription_login_orga, get_all_competition,get_equipe_details, get_joueurs_by_equipe_id, inscription_login_capitaine, inscription_capitaine_and_equipe, inscription_joueur, get_capitaine_equipe_by_login_id, get_all_teams_in_competition , get_competition_details, miseajour_statuts_compet,create_competition,recuperer_calendrier_match,classement_general
from python_lucas.connexion import connexion_capitaine, connexion_arbitre, connexion_orga

app = Flask(__name__)
app.secret_key = 'super_secret_key' 

CURRENT_COMPETITION_ID = 1

@app.route("/")
def premiere_page():
    competition = get_all_competition()
    return render_template('premiere_page.html', competition=competition)


@app.route('/premiere_page')
def retour_premiere_page ():
    return premiere_page()


@app.route("/tournois/<int:id_competition>")
def page_html(id_competition):
    competition_info = get_competition_details(id_competition)
    nombre_equipes_inscrites = len(get_all_teams_in_competition(id_competition))
    status_message = ""
    if competition_info:
        if competition_info['etat_competition'] == 0:
            equipes_restantes = competition_info['nombre_max_equipe'] - nombre_equipes_inscrites
            status_message = f"Il reste {equipes_restantes} places disponibles. Inscriptions possibles !"
        elif competition_info['etat_competition'] == 1:
            status_message = "La compétition est lancée."
        elif competition_info['etat_competition'] == 2:
            status_message = "La compétition est lancée et est dans l'état 'Tableaux'."
        else:
            status_message = "Statut de compétition inconnu."
    else:
        status_message = "Aucune compétition n'est active pour le moment."
    
    return render_template('page_principale.html', 
                           status=status_message, 
                           nom_competition = competition_info[1] if competition_info else "Compétition inconnue", 
                           id_competition = competition_info[0] if competition_info else "Compétition inconnue")


################################cote capitaine###################################

@app.route('/page_login_capitaine/<int:id_competition>')
def page_login_capitaine(id_competition):
    competition_info = get_competition_details(id_competition)
    if 'login_id' in session:
        id_equipe_existante = get_capitaine_equipe_by_login_id(session['login_id'])
        if id_equipe_existante:
            flash("Vous êtes déjà connecté et avez une équipe inscrite.", 'info')
            return redirect(url_for('afficher_equipe', id_equipe=id_equipe_existante))
    return render_template('page_login_capitaine.html', 
                           nom_competition = competition_info[1] if competition_info else "Compétition inconnue", 
                           id_competition = competition_info[0] if competition_info else "Compétition inconnue")

@app.route('/page_incrip_capitaine')
def page_incrip_capitaine():
    return render_template('page_incrip_capitaine.html')

@app.route('/inscription.capitaine', methods=['POST'])
def verif_inscription_capitaine():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        success, message = inscription_login_capitaine(identifiant, mdp)
        if success:
            flash(message, 'success')
            return redirect(url_for('page_login_capitaine'))
        else:
            flash(message, 'error') 
            return render_template('page_incrip_capitaine.html')
    return redirect(url_for('page_incrip_capitaine'))

@app.route('/connexion_capitaine', methods=['POST'])
def connexion_capitaine2():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion_capitaine(identifiant, mdp):
            session['login_id'] = identifiant 
            id_equipe_existante = get_capitaine_equipe_by_login_id(identifiant)           
            if id_equipe_existante:
                flash("Connexion réussie ! Vous avez déjà une équipe inscrite.", 'success')
                return redirect(url_for('afficher_equipe', id_equipe=id_equipe_existante))
            else:
                flash("Connexion réussie ! Veuillez inscrire votre équipe.", 'success')
                return redirect(url_for('inscription_equipe_form'))
        else:
            flash("Identifiant ou mot de passe incorrect.", 'error')
            return render_template('page_login_capitaine.html', param="Identifiant ou mot de passe incorrect")
    return redirect(url_for('page_login_capitaine')) 

#jia bien modifie et simplifier car le cas ou les champs ne sont pas rempli vont etre gere en html pour plus de simplicite cote utilisateur!

@app.route('/form_inscription_equipe/<int:id_competition>', methods=['POST'])
def gerer_inscription_equipe_joueurs(id_competition):
    if request.method == 'POST':
        if 'login_id' not in session:
            flash("Vous devez être connecté pour inscrire une équipe.", 'error')
            return redirect(url_for('page_login_capitaine'))
        id_login_capitaine = session['login_id']
        id_equipe_existante = get_capitaine_equipe_by_login_id(id_login_capitaine)
        if id_equipe_existante is not None:
            flash("Vous avez déjà inscrit une équipe. Vous ne pouvez pas en inscrire une deuxième.", 'warning')
            return redirect(url_for('afficher_equipe', id_equipe=id_equipe_existante))
        nom_capitaine = request.form.get('nom_capitaine')
        prenom_capitaine = request.form.get('prenom_capitaine')
        nom_equipe = request.form.get('nom_equipe')
        competition_info = get_competition_details(id_competition)
        id_equipe, message_equipe = inscription_capitaine_and_equipe(
            nom_capitaine, prenom_capitaine, nom_equipe, id_login_capitaine, id_competition = competition_info[0], nom_competition = competition_info[1]
        )
        if id_equipe is not None:
            flash(message_equipe, 'success') 
            for i in range(1, 6): 
                prenom_joueur = request.form.get(f'prenom_player{i}')
                nom_joueur = request.form.get(f'nom_player{i}')
                if prenom_joueur and nom_joueur: 
                    success_joueur, message_joueur = inscription_joueur(nom_joueur, prenom_joueur, id_equipe)
                    if not success_joueur:
                        flash(message_joueur, 'warning') 
                else:
                    flash(f"Le joueur {i} n'a pas été entièrement renseigné et n'a pas été inscrit.", 'info')
            return redirect(url_for('afficher_equipe', id_equipe=id_equipe))
        else:
            flash(message_equipe, 'error') 
            return render_template('page_capitaine.html')
    return redirect(url_for('page_html'))

@app.route('/afficher_equipe/<int:id_equipe>/<int:id_competition>')
def afficher_equipe(id_equipe, id_competition):
    equipe_details = get_equipe_details(id_equipe)
    joueurs = get_joueurs_by_equipe_id(id_equipe)
    competition_info = get_competition_details(id_competition)
    
    if equipe_details:
        return render_template('afficher_equipe.html', equipe=equipe_details, joueurs=joueurs, 
                               nom_competition = competition_info[1] if competition_info else "Compétition inconnue", 
                               id_competition = competition_info[0] if competition_info else "Compétition inconnue")
    else:
        flash("Équipe non trouvée ou erreur de récupération.", 'error')
        return redirect(url_for('inscription_equipe_form'))
    
@app.route('/inscription_equipe_form')
def inscription_equipe_form():
    if 'login_id' not in session:
        flash("Vous devez être connecté pour inscrire une équipe.", 'error')
        return redirect(url_for('page_login_capitaine'))
    id_equipe_existante = get_capitaine_equipe_by_login_id(session['login_id'])
    
    if id_equipe_existante:
        flash("Vous avez déjà inscrit une équipe. Redirection vers votre page d'équipe.", 'warning')
        return redirect(url_for('afficher_equipe', id_equipe=id_equipe_existante))
    return render_template('page_capitaine.html')

@app.route('/logout')
def logout():
    session.pop('login_id', None) # Supprime l'identifiant de connexion de la session
    flash("Vous avez été déconnecté.", 'info')
    return redirect(url_for('premiere_page'))



################################cote spectateur##########################
@app.route('/page_spectateur/<int:id_competition>')
def page_spectateur(id_competition):
    competition_info = get_competition_details(id_competition)
    equipes = get_all_teams_in_competition(id_competition)
    classement_final = None # Initialiser le classement à None

    if competition_info:
        if competition_info['etat_competition'] == 2:
            classement_final = classement_general(id_competition)
            conn = get_db_connection()
            cursor = conn.cursor()
            for equipe_stats in classement_final:
                cursor.execute("SELECT nom_equipe FROM Equipe WHERE idEquipe = ?", (equipe_stats['idequipe'],))
                result = cursor.fetchone()
                equipe_stats['nom_equipe'] = result['nom_equipe'] if result else 'Nom Inconnu'
            conn.close()

    return render_template(
        'page_spectateur.html', 
        competition=competition_info,
        equipes=equipes, 
        classement=classement_final, # Passer le classement au template
        nom_competition=competition_info['nom_competition'] if competition_info else "Compétition inconnue", 
        id_competition=id_competition
    )
################################cote organisateur##########################
@app.route('/page_orga/<int:id_competition>')
def page_orga(id_competition):
    competition_info = get_competition_details(id_competition)
    current_status = -1
    nom_competition_display = "Compétition inconnue" 

    if competition_info:
        current_status = competition_info['etat_competition']
        nom_competition_display = competition_info['nom_competition']
        
    if current_status == 0:
        message_spectateur = "Voici la liste des équipes inscrites pour le moment :"

    elif current_status == 1:
        message_spectateur = "La compétition est en cours (Phase de poules). Plus de détails bientôt !"

    elif current_status == 2:
        message_spectateur = "La compétition est en cours (Phase de tableaux). Plus de détails bientôt !"

    else:
        message_spectateur = "Statut de compétition inconnu."
        if not competition_info: # Si aucune compétition n'a été trouvée du tout
            message_spectateur = "Aucune compétition n'est active pour le moment."

    return render_template('page_orga.html',
                           current_status=current_status,
                           competition_info=competition_info, # Passez l'objet entier si vous en avez besoin dans le template
                           nom_competition=nom_competition_display, # Le nom de la compétition pour affichage
                           id_competition=competition_info[0], # L'ID de la compétition du paramètre URL
                           message_spectateur=message_spectateur)


@app.route('/update_competition_status/<int:id_competition>/<int:status>', methods=['POST'])
def update_status(status, id_competition):
    competition_info = get_competition_details(id_competition)
    success, message = miseajour_statuts_compet(competition_info[0], status)
    if status == 1:
        tableau = generer_calendrier_round_robin(competition_info[0])
    elif status == 2:
        classement = classement_general(id_competition)
    if success:
        flash(f"Statut de la compétition : {status}. {message}", 'success')
    else:
        flash(f"Erreur lors de la mise à jour du statut : {message}", 'error')
    return redirect(url_for('page_orga', id_competition = competition_info[0]))

@app.route('/page_login_orga')
def login_orga ():
    return render_template('page_login_orga.html')

@app.route('/page_incrip_orga')
def inscrip_orga():
    return render_template('page_incrip_orga.html')

@app.route('/creer_tournoi', methods=['GET', 'POST'])
def creer_tournoi():
    if request.method == 'POST':
        nom_tournoi = request.form.get('nom_tournoi')
        nb_equipe_max = request.form.get('nb_equipe_max')
        if nom_tournoi and nb_equipe_max:
            success = create_competition(nom_tournoi, int(nb_equipe_max))
            if success:
                flash(f"Le tournoi '{nom_tournoi}' a été créé avec succès !", 'success')
                return redirect(url_for('premiere_page'))
            else:
                flash("Erreur lors de la création du tournoi. Le nom existe peut-être déjà.", 'error')
        else:
            flash("Veuillez remplir tous les champs du formulaire.", 'warning')
    return render_template('creer_tournoi_orga.html')

@app.route('/connexion.orga', methods=['GET', 'POST'])
def connexion_orga2 ():
    if request.method == 'POST':
        identifiant = request.form.get('id_conn')
        mdp = request.form.get('mot_dp')
        print(identifiant, mdp)
        if connexion_orga(identifiant, mdp) == True :
            # On redirige vers la nouvelle fonction 'creer_tournoi'
            return redirect(url_for('creer_tournoi'))
        else :
            erreur = "login ou mot de passe incorrect"
            return render_template('page_login_orga.html', param=erreur)
    # Si la méthode est GET, on retourne simplement la page de login
    return render_template('page_login_orga.html')
@app.route('/inscription.orga', methods=['GET', 'POST'])
def inscription_orga2():
    if request.method == 'POST' :
        identifiant = request.form.get('identifiant')
        mdp = request.form.get('mdp')
        print(identifiant, mdp)
        if inscription_login_orga(identifiant, mdp)==True:
            return render_template('page_login_orga.html')
        else :
            erreur = "inscription impossible "
            return render_template('page_incrip_orga.html', para=erreur)
    
@app.route('/page_score/<int:id_competition>')
def aller_sur_page_score(id_competition):
    competition_info = get_competition_details(id_competition)
    calendrier = recuperer_calendrier_match(competition_info[0])
    equipes_disponibles = get_all_team_names(competition_info[0])

    # Vérifier si tous les matchs ont des scores complets
    tous_scores_entres = True
    for match in calendrier:
        if match['score1'] is None and match['score2'] is None:
            tous_scores_entres = False
            break # Pas besoin de vérifier le reste si un match est incomplet

    return render_template('page_score.html',
                           calendrier=calendrier,
                           equipes_disponibles=equipes_disponibles,
                           tous_scores_entres=tous_scores_entres) # Passer le flag au template
    
@app.route('/enregistrer_score_un_match', methods=['POST'])
def enregistrer_score_un_match():
    if request.method == 'POST':
        id_match = request.form.get('id_match')
        score1 = request.form.get('score1')
        score2 = request.form.get('score2')
        if id_match and score1 is not None and score2 is not None:
                id_match_int = int(id_match)
                score1_int = int(score1)
                score2_int = int(score2)
                conn = get_db_connection()
                cursor = conn.cursor()
                sql = """
                    UPDATE Match 
                    SET score1 = ?, score2 = ? 
                    WHERE idMatch = ?
                """
                cursor.execute(sql, (score1_int, score2_int, id_match_int))
                conn.commit()        
    return redirect(url_for('aller_sur_page_score'))
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)






