import random
import time
import datetime
from flask import Flask
from flask_cors import CORS, cross_origin
from threading import Thread

app = Flask(__name__)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

methods = ("GET", "POST")

data = []
data_idx = 0

@app.route("/test", methods=methods)
@cross_origin()
def get_panel():
    print(data)
    return data


def gen_mock_data():
    global data_idx, data
    while True:
        value = random.randint(0, 100)
        print(f"Generating mock data point: {value}")
        if data_idx >= len(data):
            data.append({
                "key": value,
                "value": value,
                "time": datetime.datetime.now().isoformat(),
            })
        else:
            data[data_idx] = {
                "key": value,
                "value": value,
                "time": datetime.datetime.now().isoformat(),
            }
        data_idx += 1
        if data_idx >= 200:
            data_idx = 0
        time.sleep(1)


if __name__ == "__main__":
    gen_thread = Thread(target=gen_mock_data)
    gen_thread.start()
    app.run(host="0.0.0.0", port=3003, debug=True)
    gen_thread.join()
