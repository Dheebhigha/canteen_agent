import streamlit as st
import cv2, os, time
from services import db, face_service

db.init_db()

def capture_frame_from_webcam():
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cam.read()
    if ret:
        if not os.path.exists("captures"):
            os.makedirs("captures")
        path = f"captures/frame_{int(time.time())}.jpg"
        cv2.imwrite(path, frame)
        cam.release()
        cv2.destroyAllWindows()
        return path
    cam.release()
    cv2.destroyAllWindows()
    return None

st.title("🍽️ Canteen Face Detection System")

menu = st.sidebar.radio("Menu", ["Register", "Serve Meal", "View Users"])

if menu == "Register":
    st.header("Register New User")
    name = st.text_input("Enter Name")
    file = st.file_uploader("Upload Face Image", type=["jpg","jpeg","png"])
    if st.button("Register"):
        if name and file:
            path = f"faces/{name.replace(' ','_')}.jpg"
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            result = face_service.register_face(name, path)
            st.success(result)
        else:
            st.warning("Please enter name and upload an image")

elif menu == "Serve Meal":
    st.header("Serve Meal (Webcam Capture)")
    if st.button("Capture & Check"):
        img_path = capture_frame_from_webcam()
        if img_path:
            result, name = face_service.identify_face(img_path)
            if result == "ALLOW":
                st.success(f"✅ Welcome {name}, Meal Granted")
            elif result == "DENY_ALREADY_SERVED":
                st.error(f"❌ {name}, already served this session")
            elif result == "DENY_UNKNOWN":
                st.error("❌ Unknown face - not registered")
            else:
                st.error("⚠️ No users registered yet")

elif menu == "View Users":
    st.header("Registered Users")
    users = db.get_all_users()
    if users:
        for uid, name, _ in users:
            st.write(f"ID: {uid}, Name: {name}")
    else:
        st.write("No users registered yet.")
