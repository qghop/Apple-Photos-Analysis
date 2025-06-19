from nicegui import ui
from helpers.osxphotos_db import get_photos
import pandas as pd
import plotly.express as px
from collections import Counter

@ui.page('/people', title='People View')
def people_view():
    ui.label('People View')
    ui.link('Go Back', '/').classes('button')

    photos = get_photos()
    photos_with_people = [p for p in photos if p.person_info]
    photos_with_named_people = [photo for photo in photos_with_people if any(p != "_UNKNOWN_" for p in photo.persons)]

    # Count people
    person_counts = {}
    for photo in photos_with_named_people:
        unique_people = set(p for p in photo.persons if p != "_UNKNOWN_")
        for person in unique_people:
            if person in person_counts:
                person_counts[person] += 1
            else:
                person_counts[person] = 1
    
    # Display as table
    columns = [
        {'name': 'person', 'label': 'Name', 'field': 'person', 'required': True, 'align': 'left'},
        {'name': 'count', 'label': 'Photo Count', 'field': 'count', 'sortable': True},
    ]
    rows_gen = [
        {'person': 'All Photos', 'count': len(photos)},
        {'person': 'Photos with People', 'count': len(photos_with_people)},
        {'person': 'Photos with Named People', 'count': len(photos_with_named_people)},
    ]
    rows_p = [{'person': name, 'count': count} for name, count in sorted(person_counts.items(), key=lambda x: -x[1])]
    rows = rows_gen + rows_p

    ui.table(columns=columns, rows=rows, row_key='person')

