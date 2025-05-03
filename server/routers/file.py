from fastapi import APIRouter, File, UploadFile, FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import os
import shutil
import base64

from services.pdf_utils import pdf_to_images
from services.image_utils import generate_passport_photo

router = APIRouter()

# Ensure required directories exist
UPLOAD_DIR = "uploads"
CONVERTED_DIR = "converted"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)


@router.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body>
            <h1>Hello Team 👋</h1>
            <p>Use /docs to try image upload and resize.</p>
        </body>
    </html>
    """


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to disk
    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse({"message": "File uploaded", "filename": file.filename})


@router.post("/resize")
async def resize_image(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...),
    quality: int = Form(85),
    format: str = Form("jpeg"),
    remove_bg: bool = Form(False)  # Ensure this is Form(...)
):
    content = await file.read()
    output_path = generate_passport_photo(
        content=content,
        target_size=(width, height),
        format=format,
        quality=quality,
        remove_bg=remove_bg
    )

    with open(output_path, "rb") as f:
        image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
    
    media_type = f"image/{'jpeg' if format == 'jpg' else format}"
    return JSONResponse(
        content={
            "image_base64": base64_image,
            "format": media_type,
            "filename": output_path.split("/")[-1]
        }
    )


@router.get("/form-specs")
async def type_form():
    form_value = [
        {'name': 'SSC Form', 'id': 'ssc_form'},
        {'name': 'UPSC Form', 'id': 'upsc_form'}
    ]
    return JSONResponse({"data": form_value, "message": "Type received"})


@router.post("/pdftoimages")
async def pdftoimages(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    base64_images = pdf_to_images(pdf_bytes)

    return JSONResponse(
        content={
            "image_base64_list": base64_images,
            "format": "jpeg",
            "page_count": len(base64_images),
            "filename": file.filename
        }
    )