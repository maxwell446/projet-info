from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/organisateur')
def organisateur():
    return render_template('organisateur.html')

@app.route('/chef')
def chef():
    return render_template('chef.html')

@app.route('/arbitre')
def arbitre():
    return render_template('arbitre.html')

@app.route('/joueur')
def joueur():
    return render_template('joueur.html')

if __name__ == '__main__':
    app.run(debug=True)