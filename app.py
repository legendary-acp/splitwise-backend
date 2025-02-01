# app.py
from flask import Flask
from database import db
from routes.groups import groups_bp
from routes.expenses import expenses_bp
from routes.balances import balances_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///splitwise.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(groups_bp, url_prefix='/groups')
    app.register_blueprint(expenses_bp, url_prefix='/groups')
    app.register_blueprint(balances_bp, url_prefix='/groups')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
