from nicegui import ui
from helpers.osxphotos_db import get_photos
import pandas as pd
import plotly.express as px

@ui.page('/scores', title='Scores View')
def scores_view():
    ui.label('Scores View')
    ui.link('Go Back', '/').classes('button')

    photos = get_photos()
    photos = [p for p in photos if p.isphoto and p.exif_info and p.exif_info.camera_make and p.score] # photos taken by a camera, with score
    
    score_options = [
        'overall',
        'curation',
        'promotion',
        'highlight_visibility',
        'behavioral',
        'failure',
        'harmonious_color',
        'immersiveness',
        'interaction',
        'interesting_subject',
        'intrusive_object_presence',
        'lively_color',
        'low_light',
        'noise',
        'pleasant_camera_tilt',
        'pleasant_composition',
        'pleasant_lighting',
        'pleasant_pattern',
        'pleasant_perspective',
        'pleasant_post_processing',
        'pleasant_reflection',
        'pleasant_symmetry',
        'sharply_focused_subject',
        'tastefully_blurred',
        'well_chosen_subject',
        'well_framed_subject',
        'well_timed_shot'
    ]
    
    ui.select(
        score_options,
        value='overall',
        label='Select Scoring Criterea',
        on_change=lambda e: update_score_view(e.value)
    ).classes('w-full max-w-xs mb-4')
    
    def update_score_view(criterea):
        if hasattr(photos[0].score, criterea):
            score_list = [getattr(p.score, criterea) for p in photos]
        else:
            score_list = [p.score.overall for p in photos]
            print("Error: Defaulting to Overall Score")
            criterea = 'overall'
        fig = px.histogram(score_list, title=f"Score: {criterea}")
        plot.figure = fig
        plot.update()
    
    data = [p.score.overall for p in photos]
    fig = px.histogram(data, title=f"Score: overall)")
    plot = ui.plotly(fig).classes('w-full h-full')