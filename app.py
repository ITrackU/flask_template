from flask import Flask
from config import Config
from routes import bp as routes_bp
from models import db
from flask_wtf.csrf import CSRFProtect

# Créer l'application via l'usine de création
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialiser les extensions
    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)

    # Enregistrer les blueprints
    app.register_blueprint(routes_bp)

    return app

if __name__ == '__main__':
    app = create_app()  # Créer l'application via la fonction d'usine
    app.run(host='0.0.0.0', port=9090, debug=True)
