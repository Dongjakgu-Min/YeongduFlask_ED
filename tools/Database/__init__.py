from app import Base
from models.nclab import Documents
from sqlalchemy import exc
from requests import session


def add_element(check, elem):
    if len(check) is 0:
        try:
            Base.session.add(elem)
            Base.session.commit()
        except exc.SQLAlchemyError:
            return exc.SQLAlchemyError, 500


def add_attachment(check, elem):
    if len(check) is 0:
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
