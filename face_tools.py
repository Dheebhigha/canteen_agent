import face_recognition
import numpy as np

def encode_face(image_path):
    img = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(img)
    if len(encodings) == 0:
        return None
    return encodings[0]

def match_face(known_encodings, unknown_encoding, tolerance=0.5):
    matches = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance)
    face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        return best_match_index
    return None
