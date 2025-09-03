from services import db, face_service

db.init_db()

DATASET = {
    "Elon Musk": "faces/elon.jpg",
    "Virat Kohli": "faces/virat.jpg",
    "Alia Bhatt": "faces/alia.jpg"
}

for name, path in DATASET.items():
    print(face_service.register_face(name, path))
