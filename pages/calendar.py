from nicegui import ui
from helpers.osxphotos_db import get_photos
import pandas as pd
from plotly_calplot import calplot

@ui.page('/calendar', title='Calendar View')
def calendar_view():
    ui.label('Calendar View')
    ui.link('Go Back', '/').classes('button')
    
    photos = get_photos()
    cal_df = pd.DataFrame([
        {
            'date': p.date,
        }
        for p in photos if p.date
    ])
    
    # Convert to datetime
    cal_df['date'] = pd.to_datetime(cal_df['date'], errors='raise', utc=True)
    
    # Get min and max year values
    min_year = cal_df['date'].dt.year.min()
    max_year = cal_df['date'].dt.year.max()
    
    select_year_options = ["All"] + [year for year in range(min_year, max_year + 1)]
    ui.select(
        select_year_options,
        value='All',
        label='Select Year',
        on_change=lambda e: update_calendar(e.value, cal_df)
    ).classes('w-full max-w-xs mb-4')
    
    def update_calendar(year, df):
        if year == 'All':
            filtered_df = df
        else:
            filtered_df = df[df['date'].dt.year == int(year)].copy()
        
        num_unique_years = filtered_df['date'].dt.year.nunique()
        filtered_df['date'] = filtered_df['date'].dt.date
        filtered_df = filtered_df.groupby('date').size().reset_index(name='photo_count')
        
        # Create a calendar heatmap
        fig = calplot(
            filtered_df,
            x='date',
            y='photo_count',
            total_height=num_unique_years * 200,
            space_between_plots=0.02,
            gap=0,
            showscale=True,
            years_title=True,
            month_lines=False,
        )
        plot.figure = fig
        plot.update()
        
    cal_df_copy = cal_df.copy()
    num_unique_years = cal_df_copy['date'].dt.year.nunique()
    cal_df_copy['date'] = cal_df_copy['date'].dt.date
    cal_df_copy = cal_df_copy.groupby('date').size().reset_index(name='photo_count')
    
    # Create a calendar heatmap
    fig = calplot(
        cal_df_copy,
        x='date',
        y='photo_count',
        total_height=num_unique_years * 200,
        space_between_plots=0.02,
        gap=0,
        showscale=True,
        years_title=True,
        month_lines=False,
    )
    
    plot = ui.plotly(fig).classes('w-full h-full')