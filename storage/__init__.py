from dropbox import *
import os


dbx = Dropbox(os.getenv("STORAGE_API"))
dbx.users_get_current_account()


def upload_file(file: bytes, file_id: int, file_type: str):
    dbx.files_upload(file, f"/homeworks/{str(file_id)}.{file_type}")
    pass


def get_file(file_id: int, file_type: str) -> bytes:
    metadata, res = dbx.files_download(path=f"/Homeworks/{str(file_id)}.{file_type}")
    return res.content
