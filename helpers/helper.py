from nicegui import ui
import osxphotos
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def download_and_convert_image(photo, output_path, q):
    """Download and convert the image to WEBP format."""
    if photo.path_edited:
        path = photo.path_edited
    else:
        path = photo.path

    if path:
        image = Image.open(path).convert('RGB')
        image.save(output_path, format='WEBP', quality=q)
        return output_path
    return None