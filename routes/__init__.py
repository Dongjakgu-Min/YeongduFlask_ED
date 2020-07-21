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

    doc = Documents.query.order_by(Documents.datetime.desc()).limit(10).all()
    recent_doc = [x.as_dict() for x in doc]

    return render_template('nclab.html', documents=result, recent=recent_doc)
