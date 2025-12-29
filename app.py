import os
from flask import Flask
from flask_login import LoginManager
from model import db, User, Level
from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=True)

  
    app.config.from_object(Config)


    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.home"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

  
    from blueprints.auth import auth_bp
    from blueprints.admin import admin_bp
    from blueprints.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")

    
    with app.app_context():
        db.create_all()

        for level_name in ("foundation", "diploma"):
            if not Level.query.filter_by(name=level_name).first():
                db.session.add(Level(name=level_name))
        db.session.commit()

        default_users = [
            {"name": "thug", "role": "admin"},
            {"name": "homie", "role": "user"},
        ]

        for u in default_users:
            if not User.query.filter_by(name=u["name"]).first():
                db.session.add(User(name=u["name"], role=u["role"]))

        db.session.commit()
        print(">> Default users ensured")


    return app




if __name__ == "__main__":
    app = create_app()
    app.run()
