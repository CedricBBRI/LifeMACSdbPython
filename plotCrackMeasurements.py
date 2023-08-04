import psycopg2
import matplotlib.pyplot as plt

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
host_id_query = "SELECT DISTINCT Host_ID FROM Cracks"

# Execute the host ID query
cursor.execute(host_id_query)

# Fetch all the results
host_ids = cursor.fetchall()

# Print the list of host IDs
print("Current Host_IDs:")
for row in host_ids:
    print(row[0])

# Ask for user input for host ID
host_id = input("Please enter one of the above Host_IDs: ")

# SQL query to retrieve all unique crack IDs for a given host
crack_id_query = "SELECT DISTINCT Crack_ID FROM Cracks WHERE Host_ID = %(host_id)s"

# Execute the crack ID query
cursor.execute(crack_id_query, {'host_id': host_id})

# Fetch all the results
crack_ids = cursor.fetchall()

# Print the list of crack IDs
print("Current Crack_IDs for selected Host_ID:")
for row in crack_ids:
    print(row[0])

# Ask for user input for crack ID
crack_id = input("Please enter one of the above Crack_IDs: ")

# SQL query to retrieve measurements for the given crack ID
measurements_query = """
SELECT Time_of_Measurement, Length, Width, Depth
FROM Measurements
WHERE Crack_ID = %(crack_id)s
ORDER BY Time_of_Measurement ASC
"""

# Execute the measurements query
cursor.execute(measurements_query, {'crack_id': crack_id})

# Fetch all the results
measurements = cursor.fetchall()

# Separate the measurements by attribute
times = [row[0] for row in measurements]
lengths = [row[1] for row in measurements]
widths = [row[2] for row in measurements]
depths = [row[3] for row in measurements]

# Close the cursor and connection
cursor.close()
cnx.close()

# Plot the measurements over time
plt.figure(figsize=(12, 8))
plt.plot(times, lengths, marker='o', label='Length')
plt.plot(times, widths, marker='o', label='Width')
plt.plot(times, depths, marker='o', label='Depth')
plt.title('Crack Measurements')
plt.xlabel('Time')
plt.ylabel('Measurements')
plt.legend()
plt.show()
