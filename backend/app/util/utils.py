import shutil, os, uuid

from fastapi import UploadFile, HTTPException


def save_file(path: str, file: UploadFile, user_email: str) -> str:
    """
    Upload a file with the specified user email to the specified path and return the file path.
    """
    # generate unique file names like "admin_2b07d8d4-3c28-4a9d-8b5b-3f9c33d52678.png"
    file_name = f"{user_email.split('@')[0]}_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(path, file_name)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")
    return file_path


def remove_file(path: str, file_name: str | None = None):
    """
    Remove the specified file from the specified path or simple the file path, if file_name is None.
    """
    if file_name:
        file_path = os.path.join(path, file_name)
    else:
        file_path = path
    try:
        os.remove(file_path)
    except Exception:
        pass
