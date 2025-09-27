from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from .models import CommunityFlair, test, CommunityMember
from .. import db

flairs = Blueprint('flairs', __name__)

@flairs.route('/community/flairs/<int:community_id>', methods=['GET', 'POST'])
@login_required
def manage_flairs(community_id):
    community = test.query.get_or_404(community_id)
    # Check if the user is owner/admin of the community
    membership = CommunityMember.query.filter_by(
        user_id=current_user.id, 
        community_id=community_id
    ).first()
    
    if not membership or membership.community_role not in ["admin", "owner"]:
        flash("You don't have permission to manage flairs for this community.", "error")
        return redirect(url_for('community.view_community', community_id=community_id))
    
    if request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color', '#6c757d')
        
        if not name:
            flash("Flair name is required.", "error")
        else:
            # Check if flair with same name exists in this community
            existing_flair = CommunityFlair.query.filter_by(
                name=name, 
                community_id=community_id
            ).first()
            
            if existing_flair:
                flash(f"A flair named '{name}' already exists in this community.", "error")
            else:
                new_flair = CommunityFlair(
                    name=name,
                    color=color,
                    community_id=community_id
                )
                db.session.add(new_flair)
                db.session.commit()
                flash(f"Flair '{name}' created successfully!", "success")
    
    flairs = CommunityFlair.query.filter_by(community_id=community_id).all()
    return render_template('Create_Flair.html', 
                           user=current_user, 
                           community=community,
                           flairs=flairs)

@flairs.route('/community/<int:community_id>/flairs/delete/<int:flair_id>')
@login_required
def delete_flair(community_id, flair_id):
    community = test.query.get_or_404(community_id)
    flair = CommunityFlair.query.get_or_404(flair_id)
    
    # Verify ownership
    membership = CommunityMember.query.filter_by(
        user_id=current_user.id, 
        community_id=community_id
    ).first()
    
    if not membership or membership.community_role not in ["admin", "owner"]:
        flash("You don't have permission to delete flairs for this community.", "error")
    elif flair.community_id != community_id:
        flash("This flair doesn't belong to the specified community.", "error")
    else:
        flair_name = flair.name
        db.session.delete(flair)
        db.session.commit()
        flash(f"Flair '{flair_name}' deleted successfully!", "success")
    
    return redirect(url_for('flairs.manage_flairs', community_id=community_id))