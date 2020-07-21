from app import app, Base
from routes.nclab import views, update, download


app.register_blueprint(views.api, url_prefix='/nclab/lec')
app.register_blueprint(update.api, url_prefix='/nclab/update')
app.register_blueprint(download.api, url_prefix='/nclab/download')



