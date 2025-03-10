from typing import Dict

def get_active_sessions() -> Dict:
    """
    Dependency to get active sessions dictionary.
    In a production app, this would connect to a database.
    """
    from .routes import active_sessions
    return active_sessions
