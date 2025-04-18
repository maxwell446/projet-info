from flask import Flask, render_template, request
from python_2eme.inscription import inscription_login
from python_2eme.connexion import connexion1

app = Flask(__name__)


@app.route("/")
def page_html():
    return render_template("page_principale.html")

@app.route('/page_login.html')
def page_login():
    return render_template('page_login.html')

@app.route('/page_incrip.html')
def page_incrip():
    return render_template('page_incrip.html')

@app.route('/page3.html')
def page3():
    return render_template('page3.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login(identifiant, mdp)
    return render_template('page_incrip.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        identifiant = request.form['id_conn']
        mdp = request.form['mot_dp']
        if connexion1(identifiant, mdp) == True :
            return render_template('page1.html')
    return render_template('page_login.html')

if __name__ == '__main__':

    app.run(debug=True, use_reloader=False)