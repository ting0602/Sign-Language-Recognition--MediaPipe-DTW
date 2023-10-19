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

    # except:
    #     print("ERROR: /api/slr")
    #     return jsonify({"bool": True, "message": "錯誤，請再輸入一次"})

# @app.route('/api/get_text', methods=['POST'])
# def get_text():
#     try:
#         result = detect_result()
#         return jsonify({"message": result})
#     except:
#         print("ERROR: /api/get_text")
#         return jsonify({"message": "錯誤，請再輸入一次"})
#         # return "錯誤，請再輸入一次"
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)