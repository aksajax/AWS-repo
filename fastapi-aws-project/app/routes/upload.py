from fastapi import APIRouter, Depends, File, UploadFile

from app.auth.dependencies import get_current_user
from app.aws.s3 import upload_file_to_s3
from app.models.user import User


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    filename = upload_file_to_s3(
        file.file,
        file.filename
    )

    return {
        "message": "File uploaded successfully",
        "filename": filename
    }