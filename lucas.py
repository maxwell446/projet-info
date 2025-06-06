from flask import Flask, render_template, request, flash, redirect, url_for, session
import os

from python_lucas.inscription import get_equipe_details, get_joueurs_by_equipe_id, inscription_login_capitaine, inscription_capitaine_and_equipe, inscription_joueur, get_capitaine_equipe_by_login_id, get_all_teams_in_competition , get_competition_details, miseajour_statuts_compet
from python_lucas.connexion import connexion_capitaine

app = Flask(__name__)
app.secret_key = 'super_secret_key' 

CURRENT_COMPETITION_ID = 1

@app.route("/")
def page_html():
    competition_info = get_competition_details(CURRENT_COMPETITION_ID)
    nombre_equipes_inscrites = len(get_all_teams_in_competition(CURRENT_COMPETITION_ID))
    status_message = ""
    if competition_info:
        if competition_info['etat_competition'] == 0:
            equipes_restantes = competition_info['nombre_max_equipe'] - nombre_equipes_inscrites
            status_message = f"Il reste {equipes_restantes} places disponibles."
        elif competition_info['etat_competition'] == 1:
            status_message = "La compétition est lancée et est dans l'état 'Poules'."
        elif competition_info['etat_competition'] == 2:
            status_message = "La compétition est lancée et est dans l'état 'Tableaux'."
        else:
            status_message = "Statut de compétition inconnu."
    else:
        status_message = "Aucune compétition n'est active pour le moment."
    
    return render_template('page_principale.html', status=status_message)

################################cote capitaine##########################

@app.route('/page_login_capitaine')
def page_login_capitaine():
    if 'login_id' in session:
        id_equipe_existante = get_capitaine_equipe_by_login_id(session['login_id'])
        if id_equipe_existante:
            flash("Vous êtes déjà connecté et avez une équipe inscrite.", 'info')
            return redirect(url_for('afficher_equipe', id_equipe=id_equipe_existante))
    return render_template('page_login_capitaine.html')

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

@app.route('/form_inscription_equipe', methods=['POST'])
def gerer_inscription_equipe_joueurs():
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
        id_equipe, message_equipe = inscription_capitaine_and_equipe(
            nom_capitaine, prenom_capitaine, nom_equipe, id_login_capitaine, CURRENT_COMPETITION_ID
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

@app.route('/afficher_equipe/<int:id_equipe>')
def afficher_equipe(id_equipe):
    equipe_details = get_equipe_details(id_equipe)
    joueurs = get_joueurs_by_equipe_id(id_equipe)
    
    if equipe_details:
        return render_template('afficher_equipe.html', equipe=equipe_details, joueurs=joueurs)
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
    return redirect(url_for('page_html'))



################################cote spectateur##########################
@app.route('/page_spectateur')
def page_spectateur():
    competition_info = get_competition_details(CURRENT_COMPETITION_ID)
    equipes = []
    if competition_info:
        if competition_info['etat_competition'] == 0:
            equipes = get_all_teams_in_competition(CURRENT_COMPETITION_ID)
            message_spectateur = "Voici la liste des équipes inscrites pour le moment :"
        elif competition_info['etat_competition'] == 1:
            message_spectateur = "La compétition est en cours (Phase de poules). Plus de détails bientôt !"
            # a faire
        elif competition_info['etat_competition'] == 2:
            message_spectateur = "La compétition est en cours (Phase de tableaux). Plus de détails bientôt !"
            # a faire
        else:
            message_spectateur = "Statut de compétition inconnu."
    else:
        message_spectateur = "Aucune compétition n'est active pour le moment."

    return render_template('page_spectateur.html', competition=competition_info, equipes=equipes, message_spectateur=message_spectateur)

################################cote organisateur##########################
@app.route('/page_orga')
def page_orga():
    competition_info = get_competition_details(CURRENT_COMPETITION_ID)
    current_status = competition_info['etat_competition'] if competition_info else -1 
    return render_template('page_orga.html', current_status=current_status)

@app.route('/update_competition_status/<int:status>', methods=['POST'])
def update_status(status):
    success, message = miseajour_statuts_compet(CURRENT_COMPETITION_ID, status)
    if success:
        flash(f"Statut de la compétition mis à jour à {status} : {message}", 'success')
    else:
        flash(f"Erreur lors de la mise à jour du statut : {message}", 'error')
    return redirect(url_for('page_orga'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)