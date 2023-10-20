from flask import Flask, request, jsonify
from main import SLR_init, frame_input, detect_result


app = Flask(__name__)

@app.route('/')
def index():
    return "Success!"

@app.route('/api/init', methods=['POST'])
def init_slr():
    SLR_init()
    print("Done: init")
    return jsonify({"message": "Initialization complete"})

@app.route('/api/slr', methods=['POST'])
def send_frame():
    data = request.json
    frames = data.get('frames', [])
    # try:
    is_stop = frame_input(frames)
    result = detect_result()
    return jsonify({"bool": is_stop, "message":result})

    
if __name__ == '__main__':
    app.run(debug=True, port=8000)