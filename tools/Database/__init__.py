from app import Base
from models.nclab import Documents
from models.mail import Mails
from tools.Email.send import send_mail

from sqlalchemy import exc
from requests import session


def add_element(check, elem):
    if len(check) == 0:
        try:
            Base.session.add(elem)
            Base.session.commit()
        except exc.SQLAlchemyError:
            return exc.SQLAlchemyError, 500


def add_attachment(check, elem):
    if len(check) == 0:
        try:
            Base.session.add(elem)
            Base.session.commit()
        except exc.SQLAlchemyError:
            return exc.SQLAlchemyError, 500

        document = Documents.query.filter_by(id=elem.document_id).first()
        path = 'upload/' + elem.name
        document_session = session()
        document_session.get(document.link)
        file = document_session.get(elem.link)

        with open(path, 'wb') as writer:
            writer.write(file.content)


def add_document(docs, elem, link):
    for doc in docs:
        new_doc = Documents(doc['title'], doc['link'], link.split('_')[-1],
                            elem.semester.split('-')[0] + '-' + doc['date'], elem.id)

        doc_check = Documents.query.filter_by(link=doc['link']).all()

        if len(doc_check) == 0:
            try:
                Base.session.add(new_doc)
                Base.session.commit()
            except exc.SQLAlchemyError:
                return exc.SQLAlchemyError, 500

            sub = Mails.query.filter_by(lecture_id=elem.id)
            for p in sub:
                send_mail(p.user.email, elem.lecture_name, doc['title'])
