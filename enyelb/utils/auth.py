from flask_jwt_extended import current_user
from swingmusic.utils.auth import hash_password, check_password, get_current_userid

def get_current_username() -> str:
    """
    Get the current session user.
    """
    try:
        return current_user["name"]
    except RuntimeError:
        # Catch this error raised during migration execution
        return 'admin'

#exports for easier imports
__all__ = [
    "hash_password",
    "check_password", 
    "get_current_userid",
    "get_current_username", 
]
