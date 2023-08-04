import psycopg2
from datetime import datetime

# Predefined list of parameter names
valid_parameter_names = [
    "compressive strength",
    "strain",
    "temperature",
    "deflection"
]

# Connect to the database
cnx = psycopg2.connect(
    host='buildwise.digital',
    user='postgresCedric',
    password='postgresCedric',
    database='postgres',
    port='5438'
)

# Create a cursor object
cursor = cnx.cursor()

# SQL query to retrieve all measurement location IDs
location_id_query = "SELECT measurements_id FROM repeated_measurements"

# Execute the query
cursor.execute(location_id_query)

# Fetch all the results
location_ids = cursor.fetchall()

# Print the list of measurement location IDs
print("Current measurement location IDs:")
for row in location_ids:
    print(row[0])

# Ask for user input for measurement location ID
location_id = input("What is the measurement location ID? (Leave empty to create a new one): ")

# If measurement location ID is empty, prompt for a new entry in the 'repeated_measurements' table
if location_id == "":
    host_id = input("Enter host_id: ")
    # Split the location input into a list of strings, then convert to a list of floats
    host_location = list(map(float, input("Enter host_location (comma-separated): ").split(",")))
    description = input("Enter description: ")
    measurement_type = input("Enter measurement type: ")
    measured_by = input("Enter measured by: ")

    query = """
    INSERT INTO repeated_measurements (host_id, host_location, description, measurement_type, measured_by)
    VALUES (%(host_id)s, ARRAY[%(host_location)s], %(description)s, %(measurement_type)s, %(measured_by)s)
    RETURNING measurements_id;
    """

    # Execute the query
    cursor.execute(query, {'host_id': host_id, 'host_location': host_location, 'description': description,
                           'measurement_type': measurement_type, 'measured_by': measured_by})
    location_id = cursor.fetchone()[0]
    cnx.commit()

elif int(location_id) not in [item[0] for item in location_ids]:
    print("Invalid measurement location ID.")
    cursor.close()
    cnx.close()
    exit()

# Continue asking questions for the necessary parameters
parameter_name = input("Enter parameter_name: ")
measured_value = float(input("Enter measured_value: "))
distribution_type = input("Enter distribution_type (Leave empty if not applicable): ")

if distribution_type != "":
    standard_deviation = float(input("Enter standard_deviation: "))
else:
    standard_deviation = None

time_of_measurement = datetime.now()
measured_by = input("Enter measured by: ")
description = input("Enter description: ")

# Print the entered information and ask for confirmation
print(f'\nYou entered the following information:')
print(f'Measurement location ID: {location_id}')
print(f'Parameter Name: {parameter_name}')
# Check if the parameter name is valid
if parameter_name not in valid_parameter_names:
    print(f"Warning: {parameter_name} is not in the predefined list.")
    confirm_parameter_name = input("Do you want to continue with this parameter name? [y/n]: ")
    if confirm_parameter_name.lower() != 'y':
        print("Operation cancelled.")
        cursor.close()
        cnx.close()
        exit()
print(f'Measured Value: {measured_value}')
print(f'Distribution Type: {distribution_type}')
print(f'Standard Deviation: {standard_deviation}')
print(f'Time of Measurement: {time_of_measurement}')
print(f'Measured by: {measured_by}')
print(f'Description: {description}')

confirm = input('\nDo you want to add this information to the database? [y/n]: ')
if confirm.lower() != 'y':
    print('Operation cancelled.')
else:
    # SQL query
    query = """
    INSERT INTO measurements (measurements_id, parameter_name, measured_value, distribution_type, standard_deviation, time_of_measurement, measured_by, description)
    VALUES (%(location_id)s, %(parameter_name)s, %(measured_value)s, %(distribution_type)s, %(standard_deviation)s, %(time_of_measurement)s, %(measured_by)s, %(description)s);
    """

    # Execute the query
    cursor.execute(query, {'location_id': location_id, 'parameter_name': parameter_name, 'measured_value': measured_value,
                           'distribution_type': distribution_type, 'standard_deviation': standard_deviation, 'time_of_measurement': time_of_measurement,
                           'measured_by': measured_by, 'description': description})

    # Commit the transaction
    cnx.commit()
    print("New measurement added successfully.")

# Close the cursor and connection
cursor.close()
cnx.close()
