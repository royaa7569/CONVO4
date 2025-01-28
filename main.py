from flask import Flask, send_file
import os
import threading
import time
import requests

# Initialize Flask app
app = Flask(__name__)

# Serve the index.html file
@app.route('/')
def index():
    try:
        # Ensure the "public/index.html" file exists
        return send_file(os.path.join(os.path.dirname(__file__), "public", "index.html"))
    except FileNotFoundError:
        return "Error: 'index.html' file not found in the 'public' directory.", 404

# Set static folder for serving additional files
app.static_folder = 'public'

# Function to start the Flask server
def start_flask_server():
    port = int(os.environ.get("PORT", 3000))  # Default port is 3000
    app.run(host='0.0.0.0', port=port, debug=True)

# Function to periodically ping the server
def ping_server():
    sleep_time = 10 * 60  # Ping every 10 minutes
    url = "http://localhost:3000"  # Replace with the actual server URL

    while True:
        time.sleep(sleep_time)
        try:
            response = requests.get(url, timeout=10)
            print(f"Pinged server successfully with response: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error pinging server: {e}")

# Main block to start the server and the ping thread
if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.daemon = True  # Ensure it stops when the main thread exits
    flask_thread.start()

    # Start the ping server in the main thread
    ping_server()
