from flask import Flask
from main import SLR_init, frame_input

app = Flask(__name__)

@app.route('/api/init', methods=['POST'])
def init_slr():
    SLR_init()

@app.route('/api/slr', methods=['GET'])
def send_frame(frame):
    frame_input(frame)

if __name__ == '__main__':
    app.run(debug=True)