from flask import Blueprint, send_file
from models import Attachments
from pathlib import Path


api = Blueprint('nclab_download', __name__)


@api.route('/<file_id>')
def download(file_id):
    file = Attachments.query.filter_by(id=file_id).first()

    if file is None:
        return 'Invalid Input', 401

    filename = str(Path.cwd() / 'upload' / file.name)
    return send_file(filename, mimetype=None, attachment_filename=file.filename, as_attachment=True)
