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
    import os
    import cloudinary
    import cloudinary.uploader

    cloudinary.config( 
    cloud_name = os.getenv("degsaqcd3"), 
    api_key = os.getenv("493434864335775"), 
    api_secret = os.getenv("1raBkmg7lhVHr7fJxzutLLMPrz4")
    )
    from .models import User, test, CommunityMember
    with app.app_context():
        if os.getenv("RESET_DB", "false").lower() == "true":
            with db.engine.connect() as conn:
                conn.execute(db.text('DROP SCHEMA public CASCADE'))
                conn.execute(db.text('CREATE SCHEMA public'))
            db.create_all()
            Createmoderator()
        else:
            db.create_all()
            Createmoderator()


    from .views import views
    from .auth import auth
    from .DBinfo import DBinfo
    from .Profile import Profile
    from .PostHandle import PostHandle
    from .community import community

    app.register_blueprint(DBinfo, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Profile,url_prefix='/')
    app.register_blueprint(PostHandle,url_prefix='/')
    app.register_blueprint(community,url_prefix='/')

    from .models import User, test, CommunityMember


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