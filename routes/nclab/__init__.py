from app import app, Base
from routes.nclab import views, update


app.register_blueprint(views.api, url_prefix='/nclab/lec')
app.register_blueprint(update.api, url_prefix='/nclab/update')



