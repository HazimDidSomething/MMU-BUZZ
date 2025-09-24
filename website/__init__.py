from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import text
from flask_migrate import Migrate , upgrade


db = SQLAlchemy()
DB_name = "database.db"
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "[|_MMU_)(!BUZZ#)-=1?[|]"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://db_kscb_user:7ImyweYIfxkgFalUtfyvESGnanwafCzG@dpg-d33gn6ripnbc73e0abtg-a.oregon-postgres.render.com/db_kscb")

    db.init_app(app)
    from . import models 
    migrate = Migrate(app, db)
    import cloudinary
    import cloudinary.uploader

    cloudinary.config( 
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
        api_key = os.getenv("CLOUDINARY_API_KEY"), 
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
    )
    from .models import User, test, CommunityMember, Posts, PostsImg, PostComment
    
    with app.app_context():
        try:
            upgrade()
            print(" Database upgraded successfully!")
        except Exception as e:
            print(f"Could not upgrade database: {e}")
        '''
    TO NUKE THE DB
        if os.getenv("RESET_DB", "false").lower() == "true":
            db.session.execute(text("DROP SCHEMA public CASCADE"))
            db.session.execute(text("CREATE SCHEMA public"))
            db.session.commit()
            db.create_all()
            Createmoderator()
        else:
            db.create_all()
            Createmoderator()
        '''

    from .views import views
    from .auth import auth
    from .DBinfo import DBinfo
    from .Profile import Profile
    from .PostHandle import PostHandle
    from .community import community
    from .sign_up_otp import sign_up_otp

    app.register_blueprint(sign_up_otp, url_prefix='/')
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
                password=generate_password_hash("1234567",method ='pbkdf2:sha256'),
                Role="moderator"   
                )

                db.session.add(new_mod)
                db.session.commit()
                print("Moderator added successfully!")
    else:
                pass