from flask import render_template, redirect, session, Blueprint, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models.loginform import LoginForm, SignupForm
from models.users import Users
from app import Base

api = Blueprint("login_views", __name__)


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template("auth/login.html", form=form)
    elif request.method == "POST":
        username = request.form['id']
        password = request.form['pw']

        check = Users.query.filter_by(username=username).first()
        if check is None:
            flash('존재하지 않는 아이디입니다.')
            return redirect('/auth/login')

        if check_password_hash(check.password, password):
            session["login"] = True
            if check.is_admin is False:
                session["admin"] = False
            else:
                session["admin"] = True
            session["username"] = username
            return redirect("/")
        else:
            flash('비밀번호가 틀렸습니다.')
            return redirect("/auth/login")


@api.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        form = SignupForm()

        return render_template("auth/signup.html", form=form)
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pw']
        email = request.form['email']

        hash_pw = generate_password_hash(password)

        check = Users.query.filter_by(username=username,
                                      email=email).first()
        if check is None:
            Base.session.add(Users(username, hash_pw, email))
            Base.session.commit()
            return redirect('/auth/login')
        else:
            return redirect('/')


@api.route("/logout")
def sign_out():
    session.pop("username", None)
    session.pop("login", None)
    session.pop("admin", None)
    return redirect("/")
