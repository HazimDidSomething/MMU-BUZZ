from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import test, CommunityMember

community = Blueprint("community", __name__)

@community.route("/community")
@login_required
def all_communities():
    communities = test.query.all()
    return render_template("community.html", communities=communities)

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
