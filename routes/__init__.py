from flask import render_template
from routes.nclab import *
from models.nclab import *
from app import app


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/nclab')
def nclab_main():
    lectures = Lectures.query.all()
    result = [x.as_dict() for x in lectures]

    return render_template('nclab.html', documents=result)


@app.route('/info')
def info():
    return render_template('info.html')
