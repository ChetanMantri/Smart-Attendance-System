import os
import cv2

FACES_DIR = os.getenv('FACES_DIR', 'instance/faces')


def capture_images(user_id, name, email, parents_no):
    user_folder = f'{user_id}_{name}'
    user_folder_path = os.path.join(FACES_DIR, user_folder)

    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0

    while count < 10:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            count += 1
            face = frame[y:y+h, x:x+w]
            image_path = os.path.join(user_folder_path, f'{user_id}_{name}_{count}.jpg')
            cv2.imwrite(image_path, face)

    cap.release()
    cv2.destroyAllWindows()

    return user_folder_path


