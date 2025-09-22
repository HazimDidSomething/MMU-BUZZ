from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import test, CommunityMember, Posts

community = Blueprint("community", __name__)

@community.route("/community/<int:community_id>")
@login_required
def view_community(community_id):
    community = test.query.get_or_404(community_id)
    posts = Posts.query.filter_by(community_id=community.id).all()
    members = CommunityMember.query.filter_by(community_id=community.id).all()
    return render_template("view_community.html", community=community, posts=posts, members=members, user=current_user)
@community.route("/create_community", methods=["GET", "POST"])
def create_community():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Community name is required!", "error")
            return redirect(url_for("community.create_community"))

        new_community = test(name=name, description=description)
        db.session.add(new_community)
        db.session.commit()
        flash("Community created successfully!", "success")
        return redirect(url_for("views.home"))

    return render_template("create_community.html", user=current_user)

@community.route("/community/<int:community_id>/create_post", methods=["GET", "POST"])
@login_required
def create_post_in_community(community_id):
    community = test.query.get_or_404(community_id)

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            flash("Title and content are required", "error")
            return redirect(url_for("community.create_post_in_community", community_id=community_id))

        new_post = Posts(
            title=title,
            content=content,
            user_id=current_user.id,
            FirstName=current_user.FirstName,
            community_id=community.id
        )

        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("community.view_community", community_id=community.id))

    return render_template("create_post_in_community.html", community=community, user=current_user)
