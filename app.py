from nicegui import ui
import osxphotos
from PIL import Image
import pillow_heif
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import helper

pillow_heif.register_heif_opener()


print("Opening database, may take a moment...")
db = osxphotos.PhotosDB()
if not db:
    print("No Photos Library found. Exiting.")
    exit(1)
print("Database opened successfully.")


# Landing page
@ui.page('/landing')
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
@ui.page('/map')
def map_view():
    ui.label('Map View')
    
    # Get all location data
    photos = db.photos()
    loc_df = pd.DataFrame()
    
    loc_df = pd.DataFrame([
        {
            'latitude': p.latitude,
            'longitude': p.longitude,
            'date_str': p.date_original.strftime("%b %-d, %Y at %-I:%M %p") if p.date_original else "Unknown"
        }
        for p in photos if p.latitude and p.longitude and not p.hasadjustments
    ])
    
    fig = px.density_map(loc_df, 
                         lat='latitude', 
                         lon='longitude', 
                         radius=5, 
                         center=dict(lat=0, lon=180),
                         zoom=0,
                         map_style='carto-positron',
                         hover_name='date_str')
    
    ui.plotly(fig).classes('w-full h-[80vh]')


# Timeline View
@ui.page('/')
def timeline_view():
    ui.label('Timeline View')
    
    # Get all photos with date
    photos = db.photos()
    timeline_df = pd.DataFrame([
        {
            'date_original': p.date_original,
            'latitude': p.latitude,
            'longitude': p.longitude,
            #'utc_time': p.date_original - timedelta(seconds=p.tzoffset) if p.tzoffset else p.date_original,
        }
        for p in photos if p.date_original and p.latitude and p.longitude
    ])
    
    # Explicitly convert to datetime, sort
    timeline_df['date_original'] = pd.to_datetime(timeline_df['date_original'], errors='raise', utc=True)
    timeline_df.sort_values(by='date_original', inplace=True)
    
    # Set up the Plotly figure
    fig = go.Figure()
    fig.update_layout(
            geo=dict(
                scope='world',
                showland=True,
                showcountries=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                projection_type='natural earth',
            ),
        )
    
    # Plot paths, points for each year
    years = timeline_df['date_original'].dt.year.unique()
    year_span = years.max() - years.min()
    for year in years:
        year_df = timeline_df[timeline_df['date_original'].dt.year == year]
        
        if len(year_df) < 2:
            continue

        starts = year_df.iloc[:-1]
        ends = year_df.iloc[1:]

        num_segments = len(starts)
        lons = np.empty(num_segments * 3)
        lats = np.empty(num_segments * 3)
        lons[0::3] = starts['longitude'].values
        lons[1::3] = ends['longitude'].values
        lons[2::3] = np.nan
        lats[0::3] = starts['latitude'].values
        lats[1::3] = ends['latitude'].values
        lats[2::3] = np.nan

        color_num = ((year - years.min()) / year_span) * 255

        # Lines
        fig.add_trace(
            go.Scattergeo(
                lon=lons,
                lat=lats,
                mode='lines',
                line=dict(width=2, color=f'rgb({color_num}, 0, {255 - color_num})'),
                name=f'{year}',
                opacity=0.4
            )
        )
        
        # Points
        fig.add_trace(
            go.Scattergeo(
                lon=year_df['longitude'],
                lat=year_df['latitude'],
                mode='markers',
                marker=dict(size=3, color=f'rgb({color_num}, 0, {255 - color_num})'),
                text=year_df['date_original'].dt.strftime("%b %-d, %Y at %-I:%M %p"),
                hoverinfo='text',
                opacity=0.7,
                showlegend=False,
            )
        )
        
    ui.plotly(fig).classes('w-full h-[80vh]')


ui.run(reload=False)