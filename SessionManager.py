class SessionManager:
    _session = None

    @classmethod
    def get_session(cls, color_mode="16colors"):
        if cls._session is None:
            cls._session = SessionShared(None, color_mode)
        return cls._session

    @classmethod
    def set_session(cls, session):
        cls._session = session

class SessionShared:
    def __init__(self, session, color_mode):
        self.session = session
        self.color_mode = color_mode
      