from nicegui import ui
from helpers.osxphotos_db import get_photos
import pandas as pd
import plotly.express as px

@ui.page('/map')
def map_view():
    ui.label('Map View')
    ui.link('Go Back', '/').classes('button')

    photos = get_photos()
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
