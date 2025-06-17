from nicegui import ui
import osxphotos
from PIL import Image
import pillow_heif

def download_and_convert_image(photo, output_path):
    """Download and convert the image to JPEG format."""
    if photo.path_edited:
        path = photo.path_edited
    else:
        path = photo.path

    if path:
        image = Image.open(path).convert('RGB')
        image.save(output_path, format='JPEG', quality=90)
        return output_path
    return None