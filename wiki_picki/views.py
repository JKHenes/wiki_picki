from flask import Flask, render_template, session, redirect, url_for, request
from subprocess import call
from wiki_picki import *
from wiki_picki.sonicoc import *

WEBSITES={"Sausage":"sausage.fandom.com", "Vtubers": "virtualyoutuber.fandom.com", "Sonic fan characters":"sonicfanchara.fandom.com", "Super powers":"powerlisting.fandom.com"}

@app.route('/')
def welcome():
    return render_template('welcomeScreen.jinja')

@app.route('/search', methods=['GET', 'POST'])
def decision(name=None):
    if request.method == 'POST':
        session.clear()
        web_addr = WEBSITES[request.form['website']]
        if 'searches' in session:
            session['searches'].append( [request.form['search'], web_addr])
        else:
            session['searches'] = [[request.form['search'], web_addr]]
        return redirect(url_for('result'))
    return render_template('searchMenu.jinja', name=name)

@app.route('/result')
def result():
    search = session['searches'][0][0]
    website = session['searches'][0][1]
    print("attempting" + search + "   " + website)
    data=get_info(search,website)

    return render_template('searchresult.jinja', title=data[0],url=data[1],text=data[2],image_src=data[3])
