from nicegui import ui
import osxphotos
from PIL import Image
import pillow_heif
from datetime import datetime
import helper

pillow_heif.register_heif_opener()

print("Opening database, may take a moment...")
db = osxphotos.PhotosDB()
if not db:
    print("No Photos Library found. Exiting.")
    exit(1)
print("Database opened successfully.")

# Landing page
@ui.page('/')
def landing_page():
    ui.label('Welcome to the Photos App')
    # Button to navigate to test view 1
    ui.link('Go to Test View 1', '/test1').classes('button')
    
    # Get top photos TODO check if real photo
    photos = db.photos()
    sorted_photos = sorted([p for p in photos if p.isphoto and p.import_info is None], key=lambda p: p.score.overall, reverse=True)
    
    # Make carousel of top 5 photos
    carousel_len = 5
    output_paths = []
    if len(sorted_photos) > carousel_len:
        for i in range(carousel_len):
            output_path = f'./tmp/top10c_photo_{i}.jpg'
            output_paths.append(helper.download_and_convert_image(sorted_photos[i], output_path))
        if None not in output_paths:
            with ui.carousel(animated=True, arrows=True, navigation=True).props('height=420px'):
                for i, output_path in enumerate(output_paths):
                    with ui.carousel_slide().classes('p-0'):
                        with ui.card().tight().classes('w-[400px] h-full object-cover'):
                            ui.image(output_path).classes('p-20')
                            ui.label(sorted_photos[i].date.strftime("%b %-d, %Y at %-I:%M %p")).classes('text-center text-sm w-full')
            ui.label('Top Photos')

# Test view
@ui.page('/test1')
def test_view1():
    ui.label('Test View 1')

ui.run(reload=False)