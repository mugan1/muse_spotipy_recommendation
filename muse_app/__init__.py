from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import config
import os 
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()

DATABASE_URI = os.getenv("DATABASE_URI")

def create_app(config=None):

    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    #app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite+pysqlite:///dev_db_muse.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if app.config["ENV"] == 'production':
       app.config.from_object('config.ProductionConfig')
    else:
       app.config.from_object('config.DevelopmentConfig')

    if config is not None:
       app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from muse_app.routes import main_route
   
    app.register_blueprint(main_route.bp)

    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
