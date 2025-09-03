from services import db, sessions
from tools import face_tools

def register_face(name, image_path):
    encoding = face_tools.encode_face(image_path)
    if encoding is None:
        return f"❌ No face found in {image_path}"
    db.add_user(name, encoding)
    return f"✅ Registered {name}"

def identify_face(image_path):
    unknown = face_tools.encode_face(image_path)
    if unknown is None:
        return "DENY_UNKNOWN", None

    users = db.get_all_users()
    if not users:
        return "DENY_NO_USERS", None

    ids, names, encodings = zip(*users)
    match_index = face_tools.match_face(encodings, unknown)

    if match_index is None:
        return "DENY_UNKNOWN", None

    user_id, name = ids[match_index], names[match_index]
    session = sessions.get_current_session()

    if db.has_been_served(user_id, session):
        return "DENY_ALREADY_SERVED", name

    db.mark_served(user_id, session)
    return "ALLOW", name
