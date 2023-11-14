from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Set up the database connection
def get_db_connection():
    cnx = psycopg2.connect(
        host='buildwise.digital',
        user='postgresCedric',
        password='postgresCedric',
        database='postgres',
        port='5438'
    )
    return cnx

@app.route('/')
def index():
    return "Welcome to the SQL API!"

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    sql_query = data['query']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.commit()
        return jsonify(result)
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

#if __name__ == '__main__':
#    app.run(debug=False)


#RUN USING CONSOLE CMD: waitress-serve --port=4000 --host='0.0.0.0' API:app
