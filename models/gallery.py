from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from app import Base
import datetime


class PhotoBook(Base.Model):
    __table_name__ = 'photo_book'
    __tale_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    representation = Base.Column(Base.String(200), nullable=False)
    title = Base.Column(Base.String(50), nullable=False)
    content = Base.Column(Base.String(100), nullable=False)
    created_at = Base.Column(Base.DateTime, nullable=False)

    def __init__(self, representation, title, content):
        self.representation = representation
        self.created_at = datetime.datetime.utcnow()
        self.title = title
        self.content = content

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Photo(Base.Model):
    __table_name__ = 'photo'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    img = Base.Column(Base.String(200), nullable=False)
    filename = Base.Column(Base.String(200), nullable=False)
    photo_book_id = Base.Column(Base.Integer)
    created_at = Base.Column(Base.DateTime, nullable=False)

    def __init__(self, img, filename, photo_book_id):
        self.img = img
        self.filename = filename
        self.created_at = datetime.datetime.utcnow()
        self.photo_book_id = photo_book_id

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
