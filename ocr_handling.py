import os
from google.cloud import vision
from PIL import Image
import io

# Set up Google Cloud Vision credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ian/Downloads/virtual-bonito-398414-0712f06c51d6.json"

def get_text_from_image(image_data):
    """
    Uses Google Cloud Vision API to extract text from a given image data.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_data)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return "No text found."

class OCRError(Exception):
    """Custom exception to handle OCR errors."""
    pass