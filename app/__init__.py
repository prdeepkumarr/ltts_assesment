from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import config as Config
# from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    
    app = Flask(__name__, instance_relative_config=True)
    # Initializing the configurations for 
    Config.init_app(app)
    # the pluggable dependancies
    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    from app.models.usermodels import User

    # Importing Blueprints
    from app.token import token
    from app.crypt import crypt
    swagger = Swagger(app)

    # Registring Blueprints
    app.register_blueprint(token, url_prefix="/token")
    app.register_blueprint(crypt, url_prefix='')

    return app

if __name__ == '__main__':
    print('app')
    app = create_app()
    print('app created')
    app.run()