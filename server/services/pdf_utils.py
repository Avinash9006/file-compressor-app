from PIL import Image
from io import BytesIO
from pdf2image import convert_from_bytes
from typing import List

def image_to_pdf(image_bytes: bytes, output_path="output.pdf") -> str:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image.save(output_path, "PDF", resolution=100.0)
    return output_path


def pdf_to_images(pdf_bytes: bytes, dpi=200) -> list[Image.Image]:
    images = convert_from_bytes(pdf_bytes, dpi=dpi)
    return images



def extract_pdf_pages_as_images_in_memory(pdf_bytes: bytes, page_numbers: List[int], dpi=200) -> List[Image.Image]:
    """
    Extract specific pages from a PDF as PIL.Image objects (in memory).
    
    :param pdf_bytes: Raw PDF bytes
    :param page_numbers: List of 1-based page numbers to extract (e.g., [1, 3])
    :param dpi: DPI resolution of the output images
    :return: List of PIL.Image objects
    """
    if not page_numbers:
        return []

    min_page = min(page_numbers)
    max_page = max(page_numbers)

    # Load all pages in range, then filter
    all_images = convert_from_bytes(pdf_bytes, dpi=dpi, first_page=min_page, last_page=max_page)

    # Convert page_numbers to 0-based index relative to min_page
    selected_images = [
        img for idx, img in enumerate(all_images, start=min_page)
        if idx in page_numbers
    ]

    return selected_images


