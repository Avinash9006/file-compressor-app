from PIL import Image, ImageFilter, ImageOps 
from io import BytesIO
import os
import uuid
import imghdr
from fastapi import HTTPException
import mediapipe as mp
import cv2
import numpy as np
from rembg import remove


CONVERTED_DIR = "converted"
os.makedirs(CONVERTED_DIR, exist_ok=True)


def process_and_resize_image(content: bytes, width: int, height: int, format: str = "jpeg", quality: int = 85) -> str:
    valid_formats = {"jpeg", "png", "webp"}
    format = format.lower()
    if format not in valid_formats:
        raise HTTPException(status_code=400, detail="Unsupported format.")

    if not imghdr.what(None, h=content):
        raise HTTPException(status_code=400, detail="Invalid image file.")

    try:
        image = Image.open(BytesIO(content))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to open image.")

    resized_image = image.resize((width, height), resample=Image.LANCZOS)

    filename = f"{uuid.uuid4().hex}.{format}"
    output_path = os.path.join(CONVERTED_DIR, filename)

    save_args = {}
    if format == "jpeg":
        save_args["quality"] = quality
        save_args["optimize"] = True

    resized_image.save(output_path, format=format.upper(), **save_args)
    return output_path


def detect_face_bbox(image: np.ndarray, extra_head_ratio=0.2, neck_extension_ratio=0.4):
    mp_face = mp.solutions.face_detection.FaceDetection(model_selection=1)
    results = mp_face.process(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if results.detections:
        bbox = results.detections[0].location_data.relative_bounding_box
        h, w, _ = image.shape
        x1 = int(bbox.xmin * w)
        y1 = int(bbox.ymin * h)
        x2 = int((bbox.xmin + bbox.width) * w)
        y2 = int((bbox.ymin + bbox.height) * h)

        face_height = y2 - y1

        # Extend upward to add more space above the head
        y1_extended = max(0, y1 - int(face_height * extra_head_ratio))
        # Extend downward to include neck
        y2_extended = min(h, y2 + int(face_height * neck_extension_ratio))

        return (x1, y1_extended, x2, y2_extended)
    return None



def crop_and_center_face(image: Image.Image, bbox: tuple, target_size=(600, 800), face_ratio=0.7) -> Image.Image:
    x1, y1, x2, y2 = bbox
    face_width = x2 - x1
    face_height = y2 - y1

    target_face_height = int(target_size[1] * face_ratio)
    scale = target_face_height / face_height

    # Resize full image so face fits expected ratio
    new_width = int(image.width * scale)
    new_height = int(image.height * scale)
    image_resized = image.resize((new_width, new_height), resample=Image.LANCZOS)

    # Recalculate face coordinates after scaling
    x1_scaled = int(x1 * scale)
    y1_scaled = int(y1 * scale)
    x2_scaled = int(x2 * scale)
    y2_scaled = int(y2 * scale)
    face_center_x = (x1_scaled + x2_scaled) // 2

    # Adjust vertical crop to include chest (shift down a bit)
    # Start above head by 10%, end below chin by 20%
    crop_y1 = y1_scaled - int(0.2 * target_size[1])
    crop_y2 = y2_scaled + int(0.3 * target_size[1])

    # Ensure height equals target
    crop_height = crop_y2 - crop_y1
    if crop_height < target_size[1]:
        extra = target_size[1] - crop_height
        crop_y1 = max(0, crop_y1 - extra // 2)
        crop_y2 = crop_y1 + target_size[1]
    else:
        crop_y2 = crop_y1 + target_size[1]

    crop_x1 = face_center_x - target_size[0] // 2
    crop_x2 = crop_x1 + target_size[0]

    # Prepare canvas
    canvas = Image.new("RGB", target_size, (255, 255, 255))
    image_np = np.array(image_resized)

    crop_box = (
        max(crop_x1, 0),
        max(crop_y1, 0),
        min(crop_x2, new_width),
        min(crop_y2, new_height)
    )
    cropped = Image.fromarray(image_np).crop(crop_box)

    pad_x = max(-crop_x1, 0)
    pad_y = max(-crop_y1, 0)

    canvas.paste(cropped, (pad_x, pad_y))
    return canvas





def generate_passport_photo(content: bytes, target_size=(600, 800), face_ratio=0.85, format="jpeg", quality=90, remove_bg: bool = False) -> str:
    image = Image.open(BytesIO(content))
    image = ImageOps.exif_transpose(image).convert("RGB")  # Correct orientation
    np_image = np.array(image)

    bbox = detect_face_bbox(np_image)

    if bbox:
        if remove_bg:
            image = remove_background_and_smooth_edges(content)

        processed = crop_and_center_face(image, bbox, target_size, face_ratio)
    else:
        processed = resize_and_pad_to_target(image, target_size)

    output_path = save_image_with_quality(processed, format, quality)

    if check_file_size(output_path) > 200 * 1024:
        for q in range(quality, 70, -5):
            output_path = save_image_with_quality(processed, format, q)
            if check_file_size(output_path) <= 200 * 1024:
                break

    return output_path


def save_image_with_quality(image: Image.Image, format: str, quality: int) -> str:
    filename = f"{uuid.uuid4().hex}.{format}"
    output_path = os.path.join(CONVERTED_DIR, filename)
    save_args = {"quality": quality, "optimize": True}
    image.save(output_path, format=format.upper(), **save_args)
    return output_path

def check_file_size(file_path: str) -> int:
    """Returns the file size in bytes."""
    return os.path.getsize(file_path)

def remove_background_and_fill_white(input_bytes: bytes) -> Image.Image:
    result = remove(input_bytes)  # Assuming 'remove' is the background removal function
    image = Image.open(BytesIO(result)).convert("RGBA")
    background = Image.new("RGB", image.size, (205, 205, 205))  # White background
    background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
    return background

def remove_background_and_smooth_edges(content: bytes) -> Image:
    image = Image.open(BytesIO(content)).convert("RGBA")
    
    # First, remove the background and fill with white
    image_no_bg = remove_background_and_fill_white(content)
    
    # Convert to numpy array to manipulate pixels easily
    np_image = np.array(image_no_bg)
    
    # Create a mask for the border area around the face/subject (let's use a simple border width)
    border_width = 10  # Set the border width (adjust as needed)
    height, width, _ = np_image.shape

    # Blur only the border area: Create a mask for the border region
    mask = np.zeros((height, width), dtype=np.uint8)
    mask[border_width:-border_width, border_width:-border_width] = 255  # Inside area is kept as 255 (no blur)

    # Convert back to Image for processing
    mask_image = Image.fromarray(mask)

    # Apply blur only to the border (outside the mask area)
    blurred_image = image_no_bg.filter(ImageFilter.GaussianBlur(radius=2))

    # Combine the blurred image with the original (sharp) inside region
    np_blurred = np.array(blurred_image)
    np_combined = np_image.copy()

    # Use the mask to blend the images: inside the mask is original, outside is blurred
    np_combined[mask == 0] = np_blurred[mask == 0]

    # Convert back to Image
    final_image = Image.fromarray(np_combined)
    
    return final_image


def resize_and_pad_to_target(image: Image.Image, target_size=(600, 800), background_color=(255, 255, 255)) -> Image.Image:
    original_ratio = image.width / image.height
    target_ratio = target_size[0] / target_size[1]

    if original_ratio > target_ratio:
        # Fit to width
        new_width = target_size[0]
        new_height = int(new_width / original_ratio)
    else:
        # Fit to height
        new_height = target_size[1]
        new_width = int(new_height * original_ratio)

    resized = image.resize((new_width, new_height), Image.LANCZOS)

    # Create new background
    new_image = Image.new("RGB", target_size, background_color)
    paste_x = (target_size[0] - new_width) // 2
    paste_y = (target_size[1] - new_height) // 2
    new_image.paste(resized, (paste_x, paste_y))

    return new_image


