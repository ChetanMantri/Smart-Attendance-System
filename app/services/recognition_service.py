import os
import cv2
from db_connection import get_db_connection


def recognize_faces():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    model_path = os.getenv('MODEL_PATH', 'instance/trained_model.yml')
    recognizer.read(model_path)

    cap = cv2.VideoCapture(0)
    recognized = False
    user_id = None
    user_name = None
    message = "Unable to recognize face"

    while not recognized:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face)

            if confidence < 50:
                recognized = True
                user_id = label
                connection = get_db_connection()
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()
                user_name = user['name'] if user else "Unknown"

                cursor.execute(
                    "INSERT INTO attendance (user_id, name, timestamp, status) VALUES (%s, %s, UTC_TIMESTAMP(), 'present')",
                    (user_id, user_name)
                )
                connection.commit()
                connection.close()
                message = f"User {user_name} (ID: {user_id}) recognized successfully. Attendance marked."
                break
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return message, user_id


