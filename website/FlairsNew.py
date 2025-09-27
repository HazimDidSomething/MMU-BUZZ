from .models import Posts, PostsImg, PostComment, test, CommunityMember, User, CommunityFlair
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import current_user, login_required
from sqlalchemy.sql import func  # make sure func is imported for created_at

FlairsNew = Blueprint('FlairsNew', __name__)

@FlairsNew.route('/community/flairs/<int:community_id>', methods=['GET', 'POST'])
@login_required
def Create_Flair(community_id):
    community = test.query.get_or_404(community_id)

    if request.method == 'POST':
        flair_name = request.form.get("flair_name")
        flair_color = request.form.get("flair_color")

        if not flair_name or not flair_color:
            flash("Please provide both a name and a color for the flair.", category="error")
        else:
            new_flair = CommunityFlair(
                name=flair_name,
                color=flair_color,
                community_id=community.id
            )
            db.session.add(new_flair)
            db.session.commit()
            flash(f"Flair '{flair_name}' created successfully!", category="success")
            return redirect(url_for('views.home'))
            # ^ replace 'some_blueprint.community_page' with your actual community view endpoint

    return render_template("Create_Flair.html", user=current_user, community=community)
