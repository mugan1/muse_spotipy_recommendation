from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import config
import os 
from dotenv import load_dotenv
load_dotenv()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app(config=None):

    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if app.config["ENV"] == 'production':
       app.config.from_object('config.ProductionConfig')
    else:
       app.config.from_object('config.DevelopmentConfig')

    if config is not None:
       app.config.update(config)

 

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from muse_app.routes import main_route
   
    app.register_blueprint(main_route.bp)

    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
