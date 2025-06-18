from nicegui import ui
from helpers.osxphotos_db import get_photos
import pandas as pd
import numpy as np
import plotly.graph_objects as go

@ui.page('/timeline', name='Timeline View')
def timeline_view():
    ui.label('Timeline View')
    ui.link('Go Back', '/').classes('button')

    photos = get_photos()
    timeline_df = pd.DataFrame([
        {
            'date_original': p.date_original,
            'latitude': p.latitude,
            'longitude': p.longitude,
        }
        for p in photos if p.date_original and p.latitude and p.longitude
    ])

    timeline_df['date_original'] = pd.to_datetime(timeline_df['date_original'], errors='raise', utc=True)
    timeline_df.sort_values(by='date_original', inplace=True)

    fig = go.Figure()
    fig.update_layout(
        geo=dict(
            scope='world',
            showland=True,
            showcountries=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            projection_type='natural earth',
        )
    )

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

        fig.add_trace(
            go.Scattergeo(
                lon=year_df['longitude'],
                lat=year_df['latitude'],
                mode='markers',
                marker=dict(size=3, color=f'rgb({color_num}, 0, {255 - color_num})'),
                text=year_df['date_original'].dt.strftime("%b %-d, %Y at %-I:%M %p"),
                hoverinfo='text',
                opacity=0.7,
                showlegend=False
            )
        )

    ui.plotly(fig).classes('w-full h-[80vh]')
