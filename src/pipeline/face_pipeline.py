from pathlib import Path
import dlib
from PIL import Image
import numpy as np
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_student_faces


@st.cache_resource
def load_dlib_model():
    # Takes an image as input.
    # Detects where faces are located.
    # Returns rectangles containing the detected faces.
    detector = dlib.get_frontal_face_detector()

    # Predicts the location of 68 specific points (landmarks) on a human face.
    base_dir = Path(__file__).resolve().parents[2]
    sp_path = base_dir / "shape_predictor_68_face_landmarks.dat"
    if not sp_path.exists():
        sp_path = Path("shape_predictor_68_face_landmarks.dat")

    sp = dlib.shape_predictor(str(sp_path))

    # Converts face images into unique numerical vectors (embeddings).
    # Deep learning model trained on 1 million+ faces.
    rec_path = base_dir / "dlib_face_recognition_resnet_model_v1.dat"
    if not rec_path.exists():
        rec_path = Path("dlib_face_recognition_resnet_model_v1.dat")

    facerec = dlib.face_recognition_model_v1(str(rec_path))
    return detector, sp, facerec


def process_image(image):
    if image is None:
        return []

    if isinstance(image, Image.Image):
        image = np.array(image.convert("RGB"))
    elif hasattr(image, "read"):
        image = np.array(Image.open(image).convert("RGB"))

    detector, sp, facerec = load_dlib_model()
    faces = detector(image, 1)  # returns list of faces in the image

    embeddings_list = []
    for face in faces:
        shape = sp(image, face)  # returns 68 landmarks of the face
        embedding = facerec.compute_face_descriptor(image, shape, 1)  # returns 128-d embedding
        embeddings_list.append(np.array(embedding, dtype=np.float64))

    return embeddings_list  # returns list of 128-d face descriptors


def get_train_model():
    X = []
    y = []

    student_db = get_all_student_faces()
    if not student_db:
        return None

    for student in student_db:
        emb = student.get("face_embedding") or student.get("student_embedding")
        if emb is None:
            continue
        X.append(np.array(emb, dtype=np.float64))
        y.append(str(student.get("student_id")))

    if len(X) == 0 or len(set(y)) < 2:
        return None

    model = SVC(kernel="linear", probability=True, class_weight="balanced", random_state=42)
    model.fit(X, y)
    return model



def predict_attendance(image):
    embeddings = process_image(image)

    if not embeddings:
        return "unknown"

    test_embedding = embeddings[0]

    student_db = get_all_student_faces()
    if not student_db:
        return "unknown"

    valid_students = []

    for student in student_db:
        emb = student.get("face_embedding")
        if emb is None:
            emb = student.get("student_embedding")

        if emb is None:
            continue

        emb = np.array(emb, dtype=np.float64)

        if emb.shape != (128,):
            continue

        valid_students.append((student, emb))

    if not valid_students:
        return "unknown"

    distances = []

    for student, emb in valid_students:
        dist = float(np.linalg.norm(emb - test_embedding))
        distances.append((dist, student))

    distances.sort(key=lambda x: x[0])

    best_dist, best_student = distances[0]

    # Reject faces that are too different from registered faces.
    if best_dist >= 0.50:
        return "unknown"

    # Reject ambiguous matches between different students.
    # Apply this check only when the second match belongs
    # to a different student.
    for second_dist, second_student in distances[1:]:
        if str(second_student.get("student_id")) != str(
            best_student.get("student_id")
        ):
            if second_dist - best_dist < 0.05:
                return "unknown"
            break

    return str(best_student.get("student_id"))
