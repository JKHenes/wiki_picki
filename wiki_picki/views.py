from flask import Flask, render_template, session, redirect
from wiki_picki import app

@app.route('/')
def welcome():
    return render_template('welcomeScreen.jinja')

@app.route('/search', methods=['GET', 'POST'])
def decision(name=None):
    if request.method == 'POST':
        if
    return render_template('searchMenu.jinja', name=name)

