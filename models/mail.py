from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

from app import app, Base


class Mails(Base.Model):
    __table_name__ = 'mails'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    lecture_id = Base.Column(Base.Integer, nullable=False)
    user_id = Base.Column(Base.Integer, ForeignKey('users.id'))
    user = relationship("Users", backref=backref('mails', order_by=id))

    def __init__(self, lecture_id, user_id):
        self.lecture_id = lecture_id
        self.user_id = user_id

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
