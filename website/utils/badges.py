from .. import db
from ..models import Badge, User


def award_badge(user, badge_name: str):
    """Award a badge to a user if they don't already have it"""
    badge = Badge.query.filter_by(name=badge_name).first()
    if not badge:
        return False
    
    if badge not in user.badges:
        user.badges.append(badge)
        db.session.commit()
        return True
    return False


def check_karma_badges(user):
    """Check and award karma milestone badges"""
    badges_awarded = []
    
    if user.karma >= 2500 and not any(b.name == 'Elder' for b in user.badges):
        if award_badge(user, 'Elder'):
            badges_awarded.append('Elder')
    
    elif user.karma >= 1500 and not any(b.name == 'Legend' for b in user.badges):
        if award_badge(user, 'Legend'):
            badges_awarded.append('Legend')
    
    elif user.karma >= 1000 and not any(b.name == 'Novice' for b in user.badges):
        if award_badge(user, 'Novice'):
            badges_awarded.append('Novice')
    
    elif user.karma >= 500 and not any(b.name == 'Elite' for b in user.badges):
        if award_badge(user, 'Elite'):
            badges_awarded.append('Elite')
    
    elif user.karma >= 100 and not any(b.name == 'Rising Star' for b in user.badges):
        if award_badge(user, 'Rising Star'):
            badges_awarded.append('Rising Star')
    
    return badges_awarded


def check_community_builder_badge(user):
    """Award community builder badge if user created a community"""
    from ..models import CommunityMember
    created_communities = CommunityMember.query.filter_by(
        user_id=user.id, 
        community_role='admin'
    ).count()
    
    if created_communities >= 1 and not any(b.name == 'Community Builder' for b in user.badges):
        return award_badge(user, 'Community Builder')
    return False


def check_streak_badge(user):
    """Award streak master badge for 7+ day login streak"""
    if user.login_streak >= 7 and not any(b.name == 'Streak Master' for b in user.badges):
        return award_badge(user, 'Streak Master')
    return False


def check_post_master_badge(user):
    """Award post master badge for creating 10+ posts"""
    if len(user.posts) >= 10 and not any(b.name == 'Post Master' for b in user.badges):
        return award_badge(user, 'Post Master')
    return False


def get_user_badges(user):
    """Get all badges for a user with earned_at info"""
    from sqlalchemy import text
    result = db.session.execute(text("""
        SELECT b.name, b.description, b.icon, b.color, ub.earned_at
        FROM badges b
        JOIN user_badges ub ON b.id = ub.badge_id
        WHERE ub.user_id = :user_id
        ORDER BY ub.earned_at DESC
    """), {'user_id': user.id})
    
    return [dict(row._mapping) for row in result]
