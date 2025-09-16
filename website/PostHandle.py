from .models import Posts,PostsImg,PostComment
from flask import Blueprint ,render_template,request,flash,redirect,url_for,Request
from . import db
from flask_login import current_user,login_required,logout_user
from werkzeug.utils import secure_filename
import os
import cloudinary.uploader

UPLOAD_FOLDER = os.path.join("website", "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
PostHandle = Blueprint('post',__name__)

@PostHandle.route('/Create_Post', methods=['GET','POST'])
@login_required
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
            FirstName = current_user.FirstName,
            vote = 0
        )

        db.session.add(new_post)
        db.session.commit()
        if PIC and PIC.filename != "":
            #print("herer")

            upload_result = cloudinary.uploader.upload(PIC)
            public_id = upload_result.get("public_id")
            img_url = upload_result["secure_url"]
            img_add = PostsImg(
                post_id = new_post.id,
                name=img_url, 
                public_id=public_id,         
                mimetype=PIC.mimetype )
            db.session.add(img_add)
            db.session.commit()
        else:
            print("e")
        
        flash("Post created!", "success")
        return redirect(url_for("views.home"))
    
    return render_template("CreatePost.html", user = current_user)

@PostHandle.route("/post/<int:post_id>")
@login_required
def ViewPost(post_id):  
    post =Posts.query.get_or_404(post_id)
    img = PostsImg.query.filter_by(post_id=post_id).first()
    comments = PostComment.query.filter_by(post_id=post_id).all()
    return render_template("viewpost.html",post=post,user = current_user,img=img,comments = comments)

@PostHandle.route("/post/upvote/<int:post_id>")
@login_required
def upvote(post_id):
    if current_user.votes_remaining <= 0:
        flash("You have no votes left!", category='error')
        return redirect(url_for("post.ViewPost", post_id=post_id))
    else:
        post = Posts.query.get_or_404(post_id)
        upvote_num = Posts.vote
        post.vote = upvote_num + 1
        UserVote = current_user.votes_remaining
        current_user.votes_remaining = UserVote - 1
        print(current_user.votes_remaining)
        print("upvote")
        db.session.commit()
        img = PostsImg.query.filter_by(post_id=post_id).first()

        return redirect(url_for("post.ViewPost", post_id=post_id))

@PostHandle.route("/post/downvote/<int:post_id>")
@login_required
def downvote(post_id):
    if current_user.votes_remaining <= 0:
        flash("You have no votes left!", category='error')
        return redirect(url_for("post.ViewPost", post_id=post_id))
    else:
        post = Posts.query.get_or_404(post_id)
        downvote_num = Posts.vote
        post.vote = downvote_num -  1
        UserVote = current_user.votes_remaining
        current_user.votes_remaining = UserVote - 1
        print(current_user.votes_remaining)
        print("downvote")
        db.session.commit()
        img = PostsImg.query.filter_by(post_id=post_id).first()

        return redirect(url_for("post.ViewPost", post_id=post_id))

@PostHandle.route("/post/delete/<int:post_id>")
@login_required
def delete(post_id):

    if current_user.Role ==  "moderator":
        post = Posts.query.get_or_404(post_id)
        for img in post.images:
            cloudinary.uploader.destroy(img.public_id)
            db.session.delete(img)
            
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("views.home"))
    else:
        logout_user()
        flash("what are u doing ? XD ", category='error')
        return redirect(url_for('auth.login'))
@PostHandle.route("/post/comment/<int:post_id>", methods = ['POST'])
@login_required
def comment(post_id):
    if request.method == 'POST':
        comment = request.form.get("comment")
        new_comment = PostComment(
            post_id = post_id,
            content = comment,
            user_id = current_user.id,
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("post.ViewPost", post_id=post_id))

