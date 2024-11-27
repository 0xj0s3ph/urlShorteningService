from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join("instance", "app.db")}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    # Register routes (blueprints)
    with app.app_context():
        db.create_all()

    return app
