import datetime

def get_current_session():
    now = datetime.datetime.now().time()
    if now < datetime.time(12, 0):
        return "morning"
    else:
        return "evening"
