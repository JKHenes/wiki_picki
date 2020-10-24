from flask import Flask
from flask import render_template
from wiki_picki import app

@app.route('/')
def welcome():
    return render_template('welcomeScreen.html')

@app.route('/search')
def decision(name=None):
    return render_template('searchMenu.html', name=name)

