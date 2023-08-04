import psycopg2
from datetime import datetime

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

# Ask for user input for measurements
length = input("Please enter the length of the crack: ")
width = input("Please enter the width of the crack: ")
depth = input("Please enter the depth of the crack: ")

# Get current time
now = datetime.now()

# Print the entered information and ask for confirmation
print(f'\nYou entered the following information:')
print(f'Crack_ID: {crack_id}')
print(f'Length: {length}')
print(f'Width: {width}')
print(f'Depth: {depth}')
print(f'Time of Measurement: {now}')

confirm = input('\nDo you want to add this information to the database? [y/n]: ')
if confirm.lower() != 'y':
    print('Operation cancelled.')
else:
    # SQL query
    query = """
    INSERT INTO Measurements (Crack_ID, Time_of_Measurement, Length, Width, Depth)
    VALUES (%(crack_id)s, %(time)s, %(length)s, %(width)s, %(depth)s);
    """

    # Execute the query with parameters
    cursor.execute(query, {'crack_id': crack_id, 'time': now, 'length': length, 'width': width, 'depth': depth})

    # Commit the transaction
    cnx.commit()

    print("New measurement added successfully.")

# Close the cursor and connection
cursor.close()
cnx.close()
