"""
Heatmap by city
===============

Plot a heatmap of monthly average temperatures for a set of cities.
"""
from collections import OrderedDict
import cdstoolbox as ct

# Define dictionary of cities to extract data from
cities = OrderedDict({
    'Timbuktu': {'lat': 16.7666, 'lon': 3.0026},
    'Havana': {'lat': 23.1136, 'lon': -82.3666},
    'Sydney': {'lat': -33.8688, 'lon': 151.2093},
    'Santiago': {'lat': -33.4489, 'lon': -70.6693},
    'Reykjavik': {'lat': 64.1466, 'lon': -21.9426},
})

# Define label, latitude and longitude lists
city_labels = list(cities.keys())
lats = [cities[k]['lat'] for k in cities.keys()]
lons = [cities[k]['lon'] for k in cities.keys()]


# Initialise the application
@ct.application(title='Heatmap by city')
# Define a livefigure output for the application
@ct.output.livefigure()
def application():
    """Define a function that extracts monthly average Near Surface Air Temperature for five predefined cities and plot them on a heatmap.

    Application main steps:

    - retrieve temperature gridded data
    - extract data at given locations using ct.observation.interp_from_grid
    - plot data as a heatmap
    """

    # Retrieve monthly average temperature
    data = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': '2m_temperature',
            'year': '2018',
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12'
            ],
            'time': '00:00',
            'grid': ['1', '1']
        }
    )

    # Interpolate data for the defined list of cities
    cities_temperature = ct.observation.interp_from_grid(data, lat=lats, lon=lons)

    # Plot the temperature data for each city as a heatmap with time on the x axis
    fig = ct.chart.heatmap(
        cities_temperature,
        xdim='time',
        yticks=city_labels,  # assign the city's name to the y ticks
        layout_kwargs={
            'title': 'Monthly 2m average temperature in 2018'
        }
    )

    return fig
