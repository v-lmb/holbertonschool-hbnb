from flask import Flask, render_template
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# --- Extensions instantiated at module level ---
# Created here so they can be imported anywhere:
#   from app import db, bcrypt
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Application Factory: creates and configures the Flask app.
    config_class : string du chemin vers la classe de config
                   (ex: "config.DevelopmentConfig")
    """
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    app.config.from_object(config_class)

    # Initialize extensions with the app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)

    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT token — format: Bearer <token>'
        }
    }

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/',
        authorizations=authorizations,
        security='Bearer'
    )

    # Imports inside the function to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    @app.errorhandler(404)
    def not_found(e):
        return app.send_static_file('404.html'), 404

    return app
