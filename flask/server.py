import time
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route('/stream', methods=['POST'])
def handle_stream():
    data = request.get_json()
    user_location = data['data']
    timestamp = data["timestamp"]
    return jsonify({"output": user_location['x'] + user_location['y'], "timestamp": time.time(), "server_latency": time.time() - timestamp}, 200)
    

@app.route("/")
def index():
    return "<h1>Hello<h1>"

if __name__ == '__main__':
    # Start Flask server on a port over 1024
    app.run(threaded=True)