import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import extract_text
from services.embedder import create_vector_store

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"Unsupported file type. Allowed: PDF, DOCX, TXT"
        )

    # Generate unique session id
    session_id = str(uuid.uuid4())

    # Save file temporarily
    file_path = os.path.join(UPLOAD_DIR, f"{session_id}{ext}")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Extract text
        text = extract_text(file_path, file.filename)

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the file. Make sure it's not empty or scanned.",
            )

        # Create vector store
        create_vector_store(text, session_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

    return {
        "session_id": session_id,
        "filename": file.filename,
        "message": "File uploaded and processed successfully",
    }
