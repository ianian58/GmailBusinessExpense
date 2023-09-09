from PIL import Image
import pytesseract
import io

def get_text_from_image(image_data):
    """
    Extract and return text from a given image data using Tesseract OCR.
    """
    image = Image.open(io.BytesIO(image_data))
    return pytesseract.image_to_string(image)
