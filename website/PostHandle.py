from .models import Posts
from flask import Blueprint ,render_template,request,flash,redirect,url_for
from . import db
from .models import User
from flask_login import current_user


PostHandle = Blueprint('post',__name__)

@PostHandle.route('/Create_Post', methods=['GET','POST'])
def CreatePost():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
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
        
        flash("Post created!", "success")
        return redirect(url_for("views.home"))
    
    return render_template("CreatePost.html", user = current_user)

@PostHandle.route("/post/<int:post_id>")
def ViewPost(post_id):
    post =Posts.query.get_or_404(post_id)
    return render_template("viewpost.html",post=post,user = current_user)