from app import app, Base, render_template
from flask import request, redirect, session
from routes.nclab import views, update, download
from models.nclab import *
from models.mail import Mails
from models.users import Users
from tools.Database import add_element


app.register_blueprint(views.api, url_prefix='/nclab/lec')
app.register_blueprint(update.api, url_prefix='/nclab/update')
app.register_blueprint(download.api, url_prefix='/nclab/download')


@app.route('/nclab', methods=['GET', 'POST'])
def nclab_main():
    if request.method == 'GET':
        lectures = Lectures.query.order_by(Lectures.semester.desc()).all()
        result = [x.as_dict() for x in lectures]

        doc = Documents.query.order_by(Documents.datetime.desc()).limit(10).all()
        recent_doc = [x.as_dict() for x in doc]

        attach = Attachments.query.order_by(Attachments.datetime.desc()).limit(10).all()
        recent_attach = [x.as_dict() for x in attach]

        if 'login' in session.keys() and session['username'] is not None:
            user = Users.query.filter_by(username=session['username']).one()
            checked = Mails.query.filter_by(user_id=user.id).all()
        else:
            checked = dict()

        return render_template('nclab/nclab.html', documents=result, recentdoc=recent_doc, recentattach=recent_attach,
                               checked=checked)
    elif request.method == 'POST':
        lectures = Lectures.query.all()

        if 'login' not in session.keys() and session['username'] is None:
            return redirect('/')

        username = session['username']
        user = Users.query.filter_by(username=username).one()

        for lec in lectures:
            if request.form.get(str(lec.id)) is not None:
                mail = Mails(lec.id, user.id)

                check = Mails.query.filter_by(lecture_id=lec.id, user_id=user.id).all()
                add_element(check, mail)
            else:
                check = Mails.query.filter_by(lecture_id=lec.id, user_id=user.id).all()
                if len(check) != 0:
                    Base.session.delete(check[0])
                    Base.session.commit()

        return redirect('/nclab')

