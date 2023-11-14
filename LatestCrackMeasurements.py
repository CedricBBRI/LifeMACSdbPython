import psycopg2

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

# Ask for user input
host_id = input("Please enter one of the above Host_IDs: ")

# SQL query
query = """
SELECT M.crack_id, M.time_of_measurement, M.length, M.width, M.depth
FROM public.measurements_cracks M
INNER JOIN (
    SELECT M_inner.crack_id, MAX(M_inner.time_of_measurement) AS Latest_Time
    FROM public.measurements_cracks M_inner
    WHERE M_inner.crack_id IN (
        SELECT C.crack_id
        FROM public.cracks C
        WHERE C.Host_ID = %(host_id)s
    )
    GROUP BY M_inner.crack_id
) SubQ ON M.crack_id = SubQ.crack_id AND M.time_of_measurement = SubQ.Latest_Time;
"""

# Execute the query with a parameter
cursor.execute(query, {'host_id': host_id})

# Fetch all the results
results = cursor.fetchall()

# Close the cursor and connection
cursor.close()
cnx.close()

# Print the results
for row in results:
    print(f'Crack_ID: {row[0]}, Time_of_Measurement: {row[1]}, Length: {row[2]}, Width: {row[3]}, Depth: {row[4]}')
