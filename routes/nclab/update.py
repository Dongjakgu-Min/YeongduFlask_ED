from flask import Blueprint
from app import app, Base
from .lecture import lecture
from .board import Board
from models.nclab import *
from sqlalchemy import exc

api = Blueprint('nclab_update', __name__)


@api.route('/lecture', methods=['GET'])
def nclab_update():
    lectures = lecture()

    for lec in lectures:
        args = [lec['name'], lec['semester'], lec['공지사항'], lec['강의자료'], lec['Q & A'], lec['Report']]
        new_lecture = Lectures(*args)

        lecture_check = Lectures.query.filter_by(lecture=lec['name'], semester=lec['semester']).all()

        if len(lecture_check) is 0:
            try:
                Base.session.add(new_lecture)
                Base.session.commit()
            except exc.SQLAlchemyError:
                return exc.SQLAlchemyError, 500

    return 'update complete', 200


@api.route('/<semester>', methods=["GET"])
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

                if len(doc_check) is 0:
                    try:
                        Base.session.add(new_doc)
                        Base.session.commit()
                    except exc.SQLAlchemyError:
                        return exc.SQLAlchemyError, 500

    return 'update complete', 200
