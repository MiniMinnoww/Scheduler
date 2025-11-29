from db.db import get_usernames

def validate_username(username):
    if not username:
        return {"error": "Username was not entered as a parameter."}
    if username not in get_usernames():
        return {"error": "Username is not valid."}