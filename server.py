from waitress import serve
import API  # Replace 'yourflaskapp' with the actual name of your Flask app module

serve(API.app, host='0.0.0.0', port=8080)  # 0.0.0.0 binds to all network interfaces
