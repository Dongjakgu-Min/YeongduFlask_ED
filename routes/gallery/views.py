from flask import Blueprint, render_template, request, session, redirect
from app import app, Base
from models.gallery import Photo, PhotoBook
from datetime import datetime
from pathlib import Path
from sqlalchemy import exc
from werkzeug.utils import secure_filename

api = Blueprint("gallery_views", __name__)


@api.route("/", methods=['GET'])
def gallery():
    imgs = PhotoBook.query.all()
    return render_template("gallery/gallery.html", imgs=imgs)


@api.route("/<photo_book_id>")
def photos(photo_book_id):
    title = PhotoBook.query.filter_by(id=photo_book_id).one()
    photo = Photo.query.filter_by(photo_book_id=photo_book_id).all()

    return render_template("gallery/photo_view.html", title=title, photo=photo)


@api.route("photo_book/upload", methods=['GET', 'POST'])
def upload_photo_book():
    if "login" not in session.keys() or session["admin"] is False:
        return "Invalid URL", 404

    if request.method == 'POST':
        img = request.files['file']
        filename = datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.' + img.filename.split('.')[-1]
        img.save(Path('static') / 'photo_book' / secure_filename(filename))

        elem = PhotoBook(str(Path('photo_book') / filename), request.form['title'], request.form['date'])

        try:
            Base.session.add(elem)
            Base.session.commit()
        except exc.SQLAlchemyError:
            return exc.SQLAlchemyError, 500

        return redirect('/')
    elif request.method == 'GET':
        return render_template('gallery/upload_photo_book.html')


@api.route("<photo_book_id>/photo/upload", methods=['GET', 'POST'])
def upload_photo(photo_book_id):
    if "login" not in session.keys() or session["admin"] is False:
        return "Invalid URL", 404

    if request.method == 'GET':
        photo = Photo.query.filter_by(photo_book_id=photo_book_id)
        return render_template('gallery/upload_photo.html', photo=photo)

    if request.method == 'POST':
        files = request.files.getlist("file[]")

        for file in files:
            file_type = file.content_type

            if file_type != 'image/jpeg':
                return 'Invalid Type'

            filename = datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.' + file.filename.split('.')[-1]
            file.save(Path('static') / 'photo' / secure_filename(filename))

            elem = Photo(str(Path('photo') / filename), filename, photo_book_id)

            try:
                Base.session.add(elem)
                Base.session.commit()
            except exc.SQLAlchemyError:
                return exc.SQLAlchemyError, 500

        return redirect('./upload')


@api.route('/photo/<photo_id>/delete', methods=['POST'])
def delete(photo_id):
    if "login" not in session.keys() or session["admin"] is False:
        return "Invalid URL", 404

    if request.method == 'POST':
        item = Photo.query.filter_by(id=int(photo_id)).one()
        Path.unlink(Path('static') / item.img)
        photo_book = item.photo_book_id

        try:
            Base.session.delete(item)
            Base.session.commit()
        except exc.SQLAlchemyError:
            return exc.SQLAlchemyError, 500

        return redirect("/gallery/" + str(photo_book) + '/photo/upload')
