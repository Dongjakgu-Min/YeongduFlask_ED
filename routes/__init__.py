from flask import render_template
from app import app


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/nclab')
def nclab():
    return render_template('nclab.html')


@app.route('/info')
def info():
    return render_template('info.html')
