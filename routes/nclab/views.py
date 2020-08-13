from flask import render_template, Blueprint, request
from flask_paginate import Pagination, get_page_parameter
from routes import nclab
from models.nclab import *
from app import app, Base

api = Blueprint('nclab_views', __name__)


@api.route('/<lec_id>/document')
def lecture_document(lec_id):
    index = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    offset = (index - 1) * per_page

    documents = Documents.query.order_by(Documents.datetime.desc()).filter_by(lecture_id=lec_id)
    documents_for_render = documents.limit(per_page).offset(offset).all()

    pagination = Pagination(page=index, total=documents.count(), search=False, record_name='documents',
                            per_page=per_page, css_framework='semantic', offset=offset)

    lecture = Lectures.query.filter_by(id=lec_id).one()
    name = lecture.lecture_name + ' (' + lecture.semester + ')'

    return render_template('nclab/lecture.html', documents=documents_for_render, name=name, pagination=pagination)


@api.route('/<lec_id>/attachment')
def lecture_attachment(lec_id):
    index = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    offset = (index - 1) * per_page

    attachments = Attachments.query.order_by(Attachments.datetime.desc()).filter_by(lecture_id=lec_id)
    attachments_for_render = attachments.limit(per_page).offset(offset).all()

    pagination = Pagination(page=index, total=attachments.count(), search=False, record_name='documents',
                            per_page=per_page, css_framework='semantic', offset=offset)

    lecture = Lectures.query.filter_by(id=lec_id).one()
    name = lecture.lecture_name + ' (' + lecture.semester + ')'

    return render_template('nclab/attachment.html', attachments=attachments_for_render, name=name, pagination=pagination)
