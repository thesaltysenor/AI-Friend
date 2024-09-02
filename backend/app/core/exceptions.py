# ai-friend/backend/app/core/exceptions.py

class APIException(Exception):
    pass

class CharacterDatabaseException(Exception):
    pass

class LMStudioException(Exception):
    pass

class ComfyUIException(Exception):
    pass

class NLPException(Exception):
    pass