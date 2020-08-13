from app import Base


class Users(Base.Model):
    __table_name__ = 'users'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    is_admin = Base.Column(Base.Boolean, nullable=False)
    username = Base.Column(Base.String(10), nullable=False)
    password = Base.Column(Base.String(300), nullable=False)
    email = Base.Column(Base.String(20), nullable=False)

    def __init__(self, username, user_pw, email):
        self.username = username
        self.password = user_pw
        self.email = email
        self.is_admin = False

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}