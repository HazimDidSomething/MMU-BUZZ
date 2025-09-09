from .models import Posts,PostsImg
from flask import Blueprint ,render_template,request,flash,redirect,url_for,Request
from . import db
from flask_login import current_user
from werkzeug.utils import secure_filename
import os

PostHandle = Blueprint('post',__name__)

@PostHandle.route('/Create_Post', methods=['GET','POST'])
def CreatePost():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        PIC = request.files.get("PIC")
        '''
        quick fix
        group_id = request.form.get("group_id")
        '''
        
        new_post = Posts(
            title = title,
            content = content,
            user_id = current_user.id,
           # group_id = group_id,
            FirstName = current_user.FirstName
        )

        db.session.add(new_post)
        db.session.commit()
        if PIC and PIC.filename != "":
            print("herer")

            filename = secure_filename(PIC.filename)
            PIC.save(os.path.join("website/static/uploads", filename))
            mimetype = PIC.mimetype
            img_add = PostsImg(
                post_id = new_post.id,
                name = filename,
                mimetype = mimetype )
            db.session.add(img_add)
            db.session.commit()
        else:
            print("e")
        
        flash("Post created!", "success")
        return redirect(url_for("views.home"))
    
    return render_template("CreatePost.html", user = current_user)

@PostHandle.route("/post/<int:post_id>")
def ViewPost(post_id):
    post =Posts.query.get_or_404(post_id)
    img = PostsImg.query.filter_by(post_id=post_id).first() 
    return render_template("viewpost.html",post=post,user = current_user,img=img)