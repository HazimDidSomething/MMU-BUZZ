from .models import Posts,PostsImg,PostComment,test,CommunityFlair,AnonymousPoll,AnonymousReveal
from flask import Blueprint ,render_template,request,flash,redirect,url_for,Request
from . import db
from flask_login import current_user,login_required,logout_user
from werkzeug.utils import secure_filename
import os
import cloudinary.uploader
from datetime import datetime
from .utils.karma import award_karma
from .utils.badges import check_post_master_badge

UPLOAD_FOLDER = os.path.join("website", "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
PostHandle = Blueprint('post',__name__)

@PostHandle.route('/Create_Post', methods=['GET','POST'])
@PostHandle.route('/Create_Post/<int:community_id>', methods=['GET','POST'])
@login_required
def CreatePost(community_id=None):
    communities = test.query.all()
    
    if request.method == "POST":
        if not community_id:
            community_id = request.form.get("community_id")
        community = test.query.get_or_404(community_id)
        title = request.form.get("title")
        content = request.form.get("content")
        flair_id = request.form.get("flair_id")
        
        # Anonymous mode fields
        is_anonymous = request.form.get("is_anonymous") == "on"
        is_secret = request.form.get("is_secret") == "on"
        reveal_type = request.form.get("reveal_type", "none")
        reveal_date = request.form.get("reveal_date")
        vote_threshold = request.form.get("vote_threshold")
        
        # Poll fields
        poll_question = request.form.get("poll_question")
        poll_multiple_choice = request.form.get("poll_multiple_choice") == "on"
        poll_expires = request.form.get("poll_expires")
        
        # Collect poll options
        poll_options = []
        for key, value in request.form.items():
            if key.startswith("poll_option_") and value.strip():
                poll_options.append(value.strip())
            
        PIC = request.files.get("PIC")
        new_post = Posts(
            title = title,
            content = content,
            user_id = current_user.id,
            community_id = community_id,
            FirstName = current_user.FirstName,
            vote = 0,
            flair_id = flair_id if flair_id else None,
            is_anonymous = is_anonymous,
            is_secret = is_secret,
            anonymous_author_id = current_user.id if is_anonymous else None
        )

        db.session.add(new_post)
        db.session.commit()
        
        # Handle anonymous reveal settings
        if is_anonymous and reveal_type != "none":
            reveal_date_obj = None
            reveal_condition = None
            
            if reveal_type == "time_delayed" and reveal_date:
                reveal_date_obj = datetime.fromisoformat(reveal_date.replace('T', ' '))
                new_post.reveal_date = reveal_date_obj
            elif reveal_type == "community_vote" and vote_threshold:
                reveal_condition = {"vote_threshold": int(vote_threshold)}
            
            anonymous_reveal = AnonymousReveal(
                post_id=new_post.id,
                reveal_type=reveal_type,
                scheduled_reveal_date=reveal_date_obj,
                reveal_condition=reveal_condition
            )
            db.session.add(anonymous_reveal)
        
        # Handle anonymous poll creation
        if is_anonymous and poll_question and len(poll_options) >= 2:
            poll_expires_obj = None
            if poll_expires:
                poll_expires_obj = datetime.fromisoformat(poll_expires.replace('T', ' '))
            
            anonymous_poll = AnonymousPoll(
                post_id=new_post.id,
                question=poll_question,
                options=poll_options,
                is_multiple_choice=poll_multiple_choice,
                expires_at=poll_expires_obj
            )
            db.session.add(anonymous_poll)
        
        db.session.commit()
        
        # Check for post master badge
        badges_awarded = []
        if check_post_master_badge(current_user):
            badges_awarded.append('Post Master')
        
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
        
        if badges_awarded:
            flash(f"Post created! 🏆 Earned badges: {', '.join(badges_awarded)}", "success")
        else:
            flash("Post created!", "success")
        return redirect(url_for("views.home"))
    community = test.query.get_or_404(community_id) if community_id else None
    flairs = CommunityFlair.query.filter_by(community_id=community_id).all() if community_id else []
    return render_template("CreatePost.html", user = current_user,communities=communities,community=community,flairs=flairs )

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
        # +5 karma to post author
        try:
            from .models import User
            author = User.query.get(post.user_id)
            if author:
                award_karma(author, 5, "post_upvote")
        except Exception:
            pass
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
        flash("Post deleted.", "success")
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

@PostHandle.route("/post/delete/comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    if current_user.Role == "moderator":
        comment = PostComment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for("post.ViewPost", post_id=comment.post_id))
    else:
        logout_user()
        flash("what are u doing ? XD ", category='error')
        return redirect(url_for('auth.login'))

@PostHandle.route("/post/report/<int:post_id>", methods=['GET', 'POST'])
@login_required
def report_post(post_id):
    post = Posts.query.get_or_404(post_id)

    if request.method == 'POST':
        reason = request.form.get('reason')
        if not reason:
            flash("Please provide a reason for reporting the post.", "error")
            return redirect(url_for("post.report_post", post_id=post_id))
        reason = f"| id - {current_user.id}  name - {current_user.FirstName} email - {current_user.email} | reason: {reason}\n"
        post.status = "reported"
        post.reasons = reason
        db.session.commit()
        flash("Post reported successfully.", "success")
        return redirect(url_for("views.home"))

    return render_template("report_post.html", post=post, user=current_user)

