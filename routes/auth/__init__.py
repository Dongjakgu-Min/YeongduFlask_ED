from app import app, Base
from routes.auth import manage


app.register_blueprint(manage.api, url_prefix='/auth')
