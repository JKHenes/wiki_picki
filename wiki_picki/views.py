from flask import Flask, render_template, session, redirect, url_for, request
from wiki_picki import app

@app.route('/')
def welcome():
    return render_template('welcomeScreen.jinja')

@app.route('/search', methods=['GET', 'POST'])
def decision(name=None):
    if request.method == 'POST':
        if 'searches' in session:
            session['searches'].append(0, [request.form['search'], request.form['website']])
        else:
            session['searches'] = [[request.form['search'], request.form['website']]]
        return redirect(url_for('result'))
    return render_template('searchMenu.jinja', name=name)

@app.route('/result')
def result():
    search = session['searches'][0][0]
    website = session['searches'][0][1]
    return render_template('searchresult.jinja', search=search, website=website)