from datetime import date, timedelta
from .. import db
from .badges import check_karma_badges, check_streak_badge


def award_karma(user, amount: int, reason: str = ""):
    user.karma = (user.karma or 0) + int(amount)
    db.session.commit()
    
    # Check for karma milestone badges
    badges_awarded = check_karma_badges(user)
    return badges_awarded


def record_login_streak(user):
    today = date.today()
    if user.last_login_date == today:
        return []
    
    badges_awarded = []
    
    if user.last_login_date == today - timedelta(days=1):
        user.login_streak = (user.login_streak or 0) + 1
    else:
        user.login_streak = 1
    
    user.last_login_date = today
    # +1 karma/day for login streak
    user.karma = (user.karma or 0) + 1
    db.session.commit()
    
    # Check for streak badge
    if check_streak_badge(user):
        badges_awarded.append('Streak Master')
    
    # Check for karma badges
    karma_badges = check_karma_badges(user)
    badges_awarded.extend(karma_badges)
    
    return badges_awarded


def badge_for(user):
    if user.karma >= 2500:
        return "Elder"
    if user.karma >= 1500:
        return "Legend"
    if user.karma >= 1000:
        return "Novice"
    if user.karma >= 500:
        return "Elite"
    if user.karma >= 100:
        return "Rising Star"
    return None
