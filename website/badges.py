from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .utils.badges import get_user_badges
from .models import Badge

badges = Blueprint('badges', __name__)

@badges.route('/badges')
@login_required
def view_badges():
    user_badges = get_user_badges(current_user)
    all_badges = Badge.query.all()
    
    # Mark which badges are earned
    earned_badge_names = {badge['name'] for badge in user_badges}
    for badge in all_badges:
        badge.earned = badge.name in earned_badge_names
    
    return render_template('badges.html', 
                         user=current_user, 
                         user_badges=user_badges,
                         all_badges=all_badges)

@badges.route('/badges/api')
@login_required
def badges_api():
    user_badges = get_user_badges(current_user)
    return jsonify({
        'earned_badges': user_badges,
        'total_badges': len(user_badges),
        'karma': current_user.karma
    })
