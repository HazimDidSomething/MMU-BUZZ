from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import test, CommunityMember, Posts
from .models import test

community = Blueprint("community", __name__)

@community.route("/community/<int:community_id>")
@login_required
def view_community(community_id):
    community = test.query.get_or_404(community_id)
    posts = Posts.query.filter_by(community_id=community.id).all()
    members = CommunityMember.query.filter_by(community_id=community.id).all()
    is_admin = CommunityMember.query.filter_by(
        community_id=community.id,
        user_id=current_user.id,
        community_role="admin"
    ).first() is not None
    return render_template("view_community.html", community=community, posts=posts, members=members, user=current_user, is_admin=is_admin)

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
        creator = CommunityMember(
            user_id=current_user.id,
            community_id=new_community.id,
            community_role="admin"
        )
        print(creator)
        db.session.add(creator)
        db.session.commit()
        flash("Community created successfully!", "success")
        return redirect(url_for("views.home"))

    return render_template("create_community.html", user=current_user)

@community.route("/community/<int:community_id>/create_post", methods=["GET", "POST"])
@login_required
def create_post_in_community(community_id):
    community = test.query.get_or_404(community_id)
    community_members = CommunityMember.query.filter_by(user_id=current_user.id, community_id=community.id).all()

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

@community.route("/community/<int:community_id>/delete", methods=["POST"])
@login_required
def delete_community(community_id):
    membership = CommunityMember.query.filter_by(
        user_id=current_user.id,
        community_id=community_id,
        community_role="admin"  
    ).first()

    if not membership and current_user.Role != "admin" and current_user.Role != "moderator": 
        flash("You do not have permission to delete this community!", "error")
        return redirect(url_for("community.view_community", community_id=community_id))

    community = test.query.get_or_404(community_id)
    db.session.delete(community)
    db.session.commit()

    flash(f"Community '{community.name}' has been deleted!", "success")
    return redirect(url_for("views.home"))


@community.route("/AllCommunity/", methods=["POST"])
@login_required
def view_all_communities():
    communities = test.query.all()
    return render_template("ViewAllCommunity.html", user=current_user, communities=communities)