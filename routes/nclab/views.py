from flask import render_template, Blueprint
from routes import nclab
from models.nclab import *
from app import app, Base

api = Blueprint('nclab_views', __name__)


@api.route('/<lec_id>')
def lecture_main(lec_id):
    documents = Documents.query.order_by(Documents.datetime.desc()).filter_by(lecture_id=lec_id).all()
    result = [x.as_dict() for x in documents]

    lecture = Lectures.query.filter_by(id=lec_id).all()
    name = lecture[0].lecture + ' (' + lecture[0].semester + ')'

    return render_template('nclab/lecture.html', documents=result, name=name)
