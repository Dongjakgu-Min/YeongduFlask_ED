from flask import Blueprint, render_template

api = Blueprint("gallery_views", __name__)


@api.route("/", methods=['GET'])
def gallery():
    return render_template("gallery/gallery.html")
