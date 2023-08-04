import psycopg2
import matplotlib.pyplot as plt
import numpy as np

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

# Ask for user input for host ID
host_id = input("Please enter a Host_ID (leave empty for all Hosts): ")

if host_id:
    # SQL query to retrieve all unique crack IDs for a given host
    crack_id_query = "SELECT DISTINCT Crack_ID FROM Cracks WHERE Host_ID = %(host_id)s"
else:
    # SQL query to retrieve all unique crack IDs
    crack_id_query = "SELECT DISTINCT Crack_ID FROM Cracks"

# Execute the crack ID query
cursor.execute(crack_id_query, {'host_id': host_id if host_id else None})

# Fetch all the results
crack_ids = cursor.fetchall()

# Print the list of crack IDs
print("Current Crack_IDs:")
for row in crack_ids:
    print(row[0])

# Ask for user input for crack ID
crack_id = input("Please enter one of the above Crack_IDs (leave empty for all Cracks): ")

# SQL query to retrieve measurements for the given crack ID
if crack_id:
    measurements_query = """
    SELECT Time_of_Measurement, Length * Width * Depth AS Volume
    FROM Measurements
    WHERE Crack_ID = %(crack_id)s
    ORDER BY Time_of_Measurement ASC
    """
else:
    measurements_query = """
    SELECT Crack_ID, Time_of_Measurement, Length * Width * Depth AS Volume
    FROM Measurements
    WHERE Crack_ID IN %(crack_ids)s
    ORDER BY Crack_ID, Time_of_Measurement ASC
    """

# Execute the measurements query
cursor.execute(measurements_query, {'crack_id': crack_id if crack_id else None, 'crack_ids': tuple(row[0] for row in crack_ids)})

# Fetch all the results
measurements = cursor.fetchall()

# Close the cursor and connection
cursor.close()
cnx.close()

# Separate the measurements by attribute and plot
plt.figure(figsize=(12, 8))
if crack_id:
    times = [row[0] for row in measurements]
    volumes = [row[1] for row in measurements]
    plt.plot(times, volumes, marker='o', label=f'Crack_ID: {crack_id}')
else:
    for i in np.unique([row[0] for row in measurements]):
        times = [row[1] for row in measurements if row[0] == i]
        volumes = [row[2] for row in measurements if row[0] == i]
        plt.plot(times, volumes, marker='o', label=f'Crack_ID: {i}')

plt.title('Crack Volume Over Time')
plt.xlabel('Time')
plt.ylabel('Volume')
plt.legend()
plt.show()

