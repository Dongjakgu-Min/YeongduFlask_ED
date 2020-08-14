from flask import render_template
from routes import nclab, gallery, auth
from models.nclab import *
from app import app


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')
