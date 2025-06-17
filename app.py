from nicegui import ui
import osxphotos
from PIL import Image
import pillow_heif
from datetime import datetime
import pandas as pd
import plotly.express as px
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
    ui.label('Landing Page')
    # Button to navigate to test view 1
    ui.link('Go to Test View 1', '/test1').classes('button')
    
    # Get top photos TODO check if real photo
    photos = db.photos()
    sorted_photos = sorted([p for p in photos 
                            if p.isphoto 
                            and p.exif_info is not None 
                            and p.exif_info.camera_make is not None], 
                           key=lambda p: p.score.overall, reverse=True)
    
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
                        with ui.card().tight().classes('w-[400px] h-[420px]'):
                            ui.image(output_path).classes('p-20 h-full w-full object-cover')
                            ui.label(sorted_photos[i].date.strftime("%b %-d, %Y at %-I:%M %p")).classes('text-center text-sm w-full')
            ui.label('Top Photos')


# Map View
@ui.page('/map/')
def map_view():
    ui.label('Map View')
    
    # Get all location data
    photos = db.photos()
    loc_df = pd.DataFrame()
    
    for p in photos:
        if p.latitude and p.longitude and not p.hasadjustments:
            loc_df = pd.concat([loc_df, pd.DataFrame({
                'latitude': [p.latitude],
                'longitude': [p.longitude],
                'magnitude': 1,
                'date': [p.date_original],
                'tz_offset': [p.tzoffset],
            })], ignore_index=True)
    
    fig = px.density_map(loc_df, lat='latitude', lon='longitude', z='magnitude', 
                         radius=30, 
                         title='Photo Locations',
                         center=dict(lat=0, lon=180), zoom=0,
                         #animation_frame=loc_df['date'].dt.year.astype(str),
                         color_continuous_scale='Viridis')
    
    ui.plotly(fig).classes('w-full h-full')

# Test view
@ui.page('/test1')
def test_view1():
    ui.label('Test View 1')

ui.run(reload=False)