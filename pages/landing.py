from nicegui import ui
from helpers import helper
from helpers.osxphotos_db import get_photos

@ui.page('/', title='Apple Photos Analytics')
def landing_page():
    ui.label('Landing Page')
    ui.link('Go to Map View', '/map').classes('button')
    ui.link('Go to Timeline View', '/timeline').classes('button')
    ui.link('Go to Calendar View', '/calendar').classes('button')
    ui.link('Go to Scores View', '/scores').classes('button')

    # photos = get_photos()
    # sorted_photos = sorted([
    #     p for p in photos if p.isphoto and p.exif_info and p.exif_info.camera_make
    # ], key=lambda p: p.score.overall, reverse=True)

    # carousel_len = 5
    # output_paths = []
    # if len(sorted_photos) > carousel_len:
    #     for i in range(carousel_len):
    #         output_path = f'./tmp/top10c_photo_{i}.webp'
    #         output_paths.append(helper.download_and_convert_image(sorted_photos[i], output_path, 70))
        
    #     if None not in output_paths:
    #         with ui.carousel(animated=True, arrows=True, navigation=True).props('height=420px'):
    #             for i, output_path in enumerate(output_paths):
    #                 with ui.carousel_slide().classes('p-0'):
    #                     with ui.card().tight().classes('w-[400px] h-[420px]'):
    #                         ui.image(output_path).classes('p-20 h-full w-full object-cover')
    #                         ui.label(sorted_photos[i].date.strftime("%b %-d, %Y at %-I:%M %p")).classes('text-center text-sm w-full')
    #         ui.label('Top Photos')
