from app import app, Base
from routes.gallery import views


app.register_blueprint(views.api, url_prefix='/gallery')
