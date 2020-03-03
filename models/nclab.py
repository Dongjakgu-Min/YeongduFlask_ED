from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from app import Base
import datetime


class Lectures(Base.Model):
    __table_name__ = 'nclab_lecture'
    __tale_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)

    semester = Base.Column(Base.String(7), nullable=False)
    lecture = Base.Column(Base.String(20), nullable=False)
    qa_link = Base.Column(Base.String(100), nullable=False)
    lec_link = Base.Column(Base.String(100), nullable=False)
    noti_link = Base.Column(Base.String(100), nullable=False)
    rep_link = Base.Column(Base.String(100), nullable=False)

    def __init__(self, lecture, semester, noti_link, lec_link, qa_link, rep_link):
        self.semester = semester
        self.lecture = lecture
        self.qa_link = qa_link
        self.lec_link = lec_link
        self.noti_link = noti_link
        self.rep_link = rep_link

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Documents(Base.Model):
    __table_name__ = 'nclab_document'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)

    lecture_id = Base.Column(Base.Integer, ForeignKey('lectures.id'), nullable=False)
    lecture = relationship("Lectures", backref=backref('nclab_document', order_by=id))

    title = Base.Column(Base.String(100), nullable=False)
    datetime = Base.Column(Base.String(100), nullable=False)
    link = Base.Column(Base.String(300), nullable=False)
    board_type = Base.Column(Base.String(5), nullable=False)

    def __init__(self, title, link, board_type, create_time, lecture_id):
        self.title = title
        self.link = link
        self.board_type = board_type
        self.lecture_id = lecture_id

        try:
            self.datetime = datetime.datetime.strptime(create_time, '%m-%d')
        except ValueError:
            self.datetime = datetime.datetime.today()

    def as_dict(self):
        result = {x.name: getattr(self, x.name) for x in self.__table__.columns}
        result['lec_name'] = self.lecture.lecture if self.lecture else None
        result['lec_semester'] = self.lecture.semester if self.lecture else None
        return result
