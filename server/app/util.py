from .models import User


def get_session_user(session) -> User:
    """Returns the User associated with the current session.

    :param session: the session
    :return: the User associated with the current session, or None if not logged in
    or the user does not exist
    """
    username = session.get("username")

    if not username:
        return None
    
    return User.query.filter_by(username=username).first()
