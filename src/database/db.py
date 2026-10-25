import bcrypt
from src.database.config import superbase


def check_teacher_exist(teacher_id):
    # Returns False if teacher exists, True if ID is available
    data = superbase.table("teachers").select("teacher_id").eq(
        "teacher_id", teacher_id
    ).execute()

    if data.data:
        return False

    return True


def create_teacher(teacher_id, name, password):
    clean_name = name.strip()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    data = superbase.table("teachers").insert({
        "teacher_id": int(teacher_id),
        "name": clean_name,
        "user_name": clean_name,
        "password": hashed_password
    }).execute()

    return data
    
def teacher_login(teacher_id, password):
    try:
        data = superbase.table("teachers").select("*").eq(
            "teacher_id", int(teacher_id)
        ).execute()

        if data.data:
            for teacher in data.data:
                stored_hash = teacher["password"].encode("utf-8")

                if bcrypt.checkpw(
                    password.encode("utf-8"),
                    stored_hash
                ):
                    return teacher

    except Exception as e:
        print(f"Authentication error: {e}")

    return None


def check_student_exist(student_id):
    # Returns False if student exists, True if ID is available
    try:
        data = superbase.table("students").select("student_id").eq(
            "student_id", int(student_id)
        ).execute()

        if data.data:
            return False

        return True
    except Exception as e:
        print(f"Error checking student existence: {e}")
        return False


def create_student(student_id, name, embedding=None):
    clean_name = name.strip()

    payload = {
        "student_id": int(student_id),
        "name": clean_name
    }
    if embedding is not None:
        if hasattr(embedding, "tolist"):
            payload["face_embedding"] = embedding.tolist()
        else:
            payload["face_embedding"] = embedding

    data = superbase.table("students").insert(payload).execute()
    return data


def student_login(student_id):
    try:
        data = superbase.table("students").select("*").eq(
            "student_id", int(student_id)
        ).execute()

        if data.data:
            return data.data[0]

    except Exception as e:
        print(f"Student login error: {e}")

    return None

def get_all_student_faces():
    try:
        data = superbase.table("students").select("*").execute()
        return data.data or []
    except Exception as e:
        print(f"Error fetching student faces: {e}")
        return []

def create_subject(subject_id, subject_code, name, section, teacher_id):
    try:
        data = superbase.table("subjects").insert({
            "subject_id": int(subject_id),
            "subject_code": subject_code,
            "name": name,
            "section": section,
            "teacher_id": int(teacher_id)
        }).execute()
        return data
    except Exception as e:
        print(f"Error creating subject: {e}")
        return None