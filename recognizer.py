import face_recognition
import cv2
import os
from face_logger import init_face_logs, log_face

# Load known faces
known_encodings = []
known_names = []

for file in os.listdir("known_faces"):
    if file.endswith(".jpg") or file.endswith(".png"):
        img = face_recognition.load_image_file(f"known_faces/{file}")
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(file.split(".")[0])

init_face_logs()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "UNKNOWN"
        status = "INTRUDER"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
            status = "AUTHORIZED"

        log_face(name, status)

        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 0) if status == "AUTHORIZED" else (0, 0, 255), 2)
        cv2.putText(frame, f"{name} ({status})", (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0) if status == "AUTHORIZED" else (0, 0, 255), 2)

    cv2.imshow("Face Recognition Agent", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
# recognizer.py
import cv2

def start_face_recognition():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Face Agent', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
