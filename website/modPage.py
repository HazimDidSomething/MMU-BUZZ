from flask import Blueprint ,render_template,request,flash,redirect,flash,url_for
from . import db
from .models import User , test, Posts , feedback
from flask_login import login_required, current_user

modPage = Blueprint('modPage',__name__)

@modPage.route('/mod-page')
@login_required
def show_db_info():
    # Get all users
    if current_user.Role ==  "moderator":
        users = User.query.order_by(User.id).all()
        communities = test.query.all()
        posts = Posts.query.all()
        community_num = test.query.count()
        posts_num = Posts.query.count() 
        user_num = User.query.count()
        feedbacks  = feedback.query.all()

        return render_template("modPage.html",feedbacks=feedbacks, user=current_user, users=users, user_num=user_num , communities=communities, community_num=community_num, posts=posts, posts_num=posts_num)

@modPage.route('/feedback', methods=['GET','POST'])
@login_required
def submit_feedback():
    if request.method == 'POST':
        content = request.form.get('feedback')
        new_feedback = feedback(
            content=content,
            user_id=current_user.id,
            Firstname=current_user.FirstName
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash("feedback submited !", "success")
        return redirect(url_for('views.home'))

    return render_template("feedback.html", user=current_user)

@modPage.route('/feedback/delete/<int:feedback_id>', methods=['POST'])
@login_required
def delete_feedback(feedback_id):
    fb = feedback.query.get_or_404(feedback_id)
    if current_user.Role  ==  "user": # or current_user.role != 'mod' depending on your model
        flash("You are not authorized to delete this feedback.", "danger")
        return redirect(url_for('views.home'))
    db.session.delete(fb)
    db.session.commit()
    flash("Feedback deleted successfully!", "success")
    return redirect(url_for('modPage.show_db_info'))
@modPage.route('/user/mod_make>', methods=['POST'])
@login_required
def make_moderator():
    if current_user.Role != "moderator":
        flash("You are not authorized to perform this action.", "danger")
        return redirect(url_for('views.home'))

    user_id = request.form.get('user_id')
    user = User.query.get(user_id)

    if user:
        user.Role = "moderator"
        db.session.commit()
        flash(f"{user.FirstName} has been promoted to moderator.", "success")
    else:
        flash("User not found.", "danger")

    return redirect(url_for('modPage.show_db_info'))