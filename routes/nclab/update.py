from flask import Blueprint
from tools.SNCP.lecture import lecture
from tools.SNCP.board import Board
from tools.SNCP.document import Document
from models.nclab import *
from sqlalchemy import exc
from tools.Database import add_element, add_attachment

api = Blueprint('nclab_update', __name__)


@api.route('/lecture', methods=['POST'])
def nclab_update():
    lectures = lecture()

    for lec in lectures:
        args = [lec['name'], lec['semester'], lec['공지사항'], lec['강의자료'], lec['Q & A'], lec['Report']]
        new_lecture = Lectures(*args)

        lecture_check = Lectures.query.filter_by(lecture=lec['name'], semester=lec['semester']).all()
        add_element(lecture_check, new_lecture)

    return 'update complete', 200


@api.route('/<semester>', methods=["POST"])
def nclab_semester(semester):
    if semester is None:
        return 404

    lectures = Lectures.query.filter_by(semester=semester).all()

    for elem in lectures:
        links = [elem.qa_link, elem.lec_link, elem.noti_link, elem.rep_link]
        for link in links:
            board_docs = Board(link)
            docs = board_docs.get_document()
            for doc in docs:
                new_doc = Documents(doc['title'], doc['link'], link.split('_')[-1],
                                    elem.semester.split('-')[0] + '-' + doc['date'], elem.id)

                doc_check = Documents.query.filter_by(link=doc['link']).all()

                add_element(doc_check, new_doc)

    return 'update complete', 200


@api.route('/attachment/<semester>', methods=['POST'])
def attachments(semester):
    lectures = Lectures.query.filter_by(semester=semester).all()

    docs = list()
    for lec in lectures:
        docs += Documents.query.filter_by(lecture_id=lec.id).all()

    for doc in docs:
        document = Document(doc.link)
        attachment = document.get_attach()

        for elem in attachment:
            new_attach = Attachments(elem['file'], elem['date'], elem['file_link'], doc.lecture_id, doc.id)
            check = Attachments.query.filter_by(link=elem['file_link']).all()

            add_attachment(check, new_attach)

    return "update complete", 200
