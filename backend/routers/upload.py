import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from services.extractor import extract_text
from services.embedder import create_vector_store
from limiter import check_limit

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB in bytes


@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    check_limit(request.client.host, "uploads")
    
    # Validate file type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"Unsupported file type. Allowed: PDF, DOCX, TXT"
        )

    # Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 2MB limit.")

    # Reset file pointer after reading
    await file.seek(0)

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
