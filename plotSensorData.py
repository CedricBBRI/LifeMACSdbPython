import psycopg2
import matplotlib.pyplot as plt
import mplcursors
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import gridplot
import numpy as np
import pandas as pd

import plotly.graph_objs as go

def remove_local_outliers(times, values, window, threshold):
    # Create a Pandas DataFrame from the times and values
    data = pd.DataFrame({'times': times, 'values': values})

    # Calculate the rolling mean and standard deviation
    rolling_mean = data['values'].rolling(window).mean()
    rolling_std = data['values'].rolling(window).std()

    # Identify outliers
    lower_bound = rolling_mean - (rolling_std * threshold)
    upper_bound = rolling_mean + (rolling_std * threshold)
    outliers = (data['values'] < lower_bound) | (data['values'] > upper_bound)

    # Remove outliers
    filtered_data = data[~outliers]

    return filtered_data['times'].tolist(), filtered_data['values'].tolist(), rolling_mean.tolist()


# Set up the database connection
cnx = psycopg2.connect(
    host='buildwise.digital',
    user='postgresCedric',
    password='postgresCedric',
    database='postgres',
    port='5438'
)

# Create a cursor object
cursor = cnx.cursor()

# SQL query to retrieve all unique host IDs
sensor_ch_id_query = "SELECT DISTINCT Sensor_Ch_ID FROM Sensors"

# Execute the host ID query
cursor.execute(sensor_ch_id_query)

# Fetch all the results
sensor_ch_ids = cursor.fetchall()

# Print the list of sensor_ch_ids
print("Current Sensor_Ch_IDs:")
for row in sensor_ch_ids:
    print(row[0])

# Ask for user input for host ID
sensor_ch_id = input("Please enter one of the above Sensor_Ch_IDs: ")

# SQL query to retrieve all unique crack IDs for a given host
sensor_id_query = "SELECT DISTINCT Sensor_ID FROM Sensors WHERE Sensor_Ch_ID = %(sensor_ch_id)s"

# Execute the crack ID query
cursor.execute(sensor_id_query, {'sensor_ch_id': sensor_ch_id})

# Fetch all the results
sensor_ids = cursor.fetchall()

# Print the list of crack IDs
print("Current Sensor_IDs for selected Sensor_Ch_ID:")
for row in sensor_ids:
    print(row[0])

# Ask for user input for crack ID
sensor_id = input("Please enter one of the above Sensor_IDs (leave blank to plot all): ")

# Ask for user input for the number of latest measurements
# If left blank, plot all measurements.
num_latest_measurements_input = input("Please enter the number of latest measurements you want to plot (leave blank to plot all): ")
num_latest_measurements = int(num_latest_measurements_input) if num_latest_measurements_input else None

# We are going to store our plots here
plots = []

# Create list of sensor ids. If no specific sensor_id is chosen, plot all sensor_ids for the chosen sensor_ch_id.
sensor_ids_list = [row[0] for row in sensor_ids] if not sensor_id else [sensor_id]

all_traces = []

for sensor_id in sensor_ids_list:
    # SQL query to retrieve measurements for the given sensor ID
    # If num_latest_measurements is None, plot all measurements.
    measurements_query = f"""
    SELECT Time_of_Measurement, sensor_value_s, sensor_value_t
    FROM Measurements_Sensors
    WHERE Sensor_ID = %(sensor_id)s
    ORDER BY Time_of_Measurement DESC
    {f'LIMIT {num_latest_measurements}' if num_latest_measurements is not None else ''}
    """

    # Execute the measurements query
    cursor.execute(measurements_query, {'sensor_id': sensor_id})

    # Fetch all the results
    measurements = cursor.fetchall()

    # Separate the measurements by attribute
    times = [row[0] for row in measurements]
    sensor_value_s = [row[1] for row in measurements]
    sensor_value_t = [row[2] for row in measurements]

    # Remove the outliers
    times2, sensor_value_t, rolling_mean = remove_local_outliers(times, sensor_value_t, 20, 10000)

    # Prepare the data for Bokeh, using original times and rolling mean, and sensor values after outlier removal
    data_sensor = ColumnDataSource(data=dict(x=times2, y=sensor_value_t))
    data_mean = ColumnDataSource(data=dict(x=times, y=rolling_mean))

    # Create a new plot
    p = figure(width=1000, height=1000, title=f"Sensor_ID: {sensor_id}")

    # Add a circle renderer for sensor values and line renderer for rolling mean
    p.circle('x', 'y', source=data_sensor, legend_label="Sensor Value", color="blue")
    p.line('x', 'y', source=data_mean, legend_label="Rolling Mean", color="red")

    # Add a hover tool
    hover = HoverTool(tooltips=[("Time", "@x"), ("Sensor Value", "@y")], renderers=[p.renderers[0]])
    hover2 = HoverTool(tooltips=[("Time", "@x"), ("Rolling Mean", "@y")], renderers=[p.renderers[1]])
    p.add_tools(hover, hover2)

    # Store the plot
    plots.append(p)

# Use gridplot() to arrange the plots in a grid
grid = gridplot([plots])

# Show the plot
show(grid)

# Close the cursor and connection
cursor.close()
cnx.close()
