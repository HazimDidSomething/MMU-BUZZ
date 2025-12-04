from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import text
from flask_migrate import Migrate , upgrade
from flask_mail import Mail, Message

from dotenv import load_dotenv
load_dotenv()  # Must be before accessing any environment variables



db = SQLAlchemy()
DB_name = "database.db"
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SUPABASE_DB_URL")
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
        db.create_all()
        '''
        try:
            upgrade()
            print(" Database upgraded successfully!")
        except Exception as e:
            print(f"Could not upgrade database: {e}")
        
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
    from .community import community
    from .views import views
    from .auth import auth
    from .modPage import modPage
    from .Profile import Profile
    from .PostHandle import PostHandle
    from .community import community
    from .signUP import signUP
    from .FlairsNew import FlairsNew 

    app.register_blueprint(signUP, url_prefix='/')
    app.register_blueprint(modPage, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Profile,url_prefix='/')
    app.register_blueprint(PostHandle,url_prefix='/')
    app.register_blueprint(community,url_prefix='/')
    app.register_blueprint(FlairsNew,url_prefix='/')

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