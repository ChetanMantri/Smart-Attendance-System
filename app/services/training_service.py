import os
import numpy as np
from PIL import Image
import cv2


def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    dataset_path = os.getenv("FACES_DIR", "instance/faces")

    if not os.path.exists(dataset_path):
        raise Exception("Dataset path does not exist: static/faces")

    for user_folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, user_folder)
        if not os.path.isdir(folder_path):
            continue
        try:
            user_id = int(user_folder.split('_')[0])
        except ValueError:
            print(f"Skipping folder {user_folder} as it does not start with an integer ID.")
            continue

        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            img = Image.open(img_path)
            img_gray = np.array(img.convert('L'))
            faces.append(img_gray)
            labels.append(user_id)

    if len(faces) > 0:
        recognizer.train(faces, np.array(labels))
        model_path = os.getenv('MODEL_PATH', 'instance/trained_model.yml')
        # Ensure model directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        recognizer.save(model_path)
        print("Model trained and saved successfully.")
    else:
        raise Exception("No faces found to train on.")


