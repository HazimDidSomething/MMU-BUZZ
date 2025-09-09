from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_name = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '[|_MMU_)(!BUZZ#)-=1?[|]'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg://root:TK3iZBD0rLadW6gqn4OcwlSHIDbvY4ie@dpg-d304ajndiees738v9dsg-a:5432/database_v3od"

    db.init_app(app)
    from .models import User, Group, GroupMember
    with app.app_context():
        db.create_all()
        Createmoderator()


    from .views import views
    from .auth import auth
    from .DBinfo import DBinfo
    from .Profile import Profile
    from .PostHandle import PostHandle

    app.register_blueprint(DBinfo, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Profile,url_prefix='/')
    app.register_blueprint(PostHandle,url_prefix='/')

    from .models import User, Group, GroupMember


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def Createmoderator():
    from .models import User
    from werkzeug.security import generate_password_hash

    if not User.query.filter_by(email="mod@mmu.edu.my").first():



                new_mod = User(
                email="mod@mmu.edu.my",
                FirstName="mod123",
                password=generate_password_hash("HAZIM171544",method ='pbkdf2:sha256'),
                Role="moderator"   
                )

                db.session.add(new_mod)
                db.session.commit()
                print("Moderator added successfully!")
    else:
                pass