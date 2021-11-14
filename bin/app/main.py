import threading
import time

import requests
from flask import Flask
from flask import request

from vasserman import settings
from vasserman.pipelines.predict import response


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    return response(data=request.form.to_dict(flat=True))


@app.route("/result_question", methods=["POST"])
def result_question():
    _ = request.form
    return {"data": "ok"}


def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.post(f"{settings.SERVER_HOST}/predict", data=settings.DUMMY_DATA_SAMPLE)
                if r.status_code == 200:
                    not_started = False
            except:
                pass
            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()


if __name__ == "__main__":
    start_runner()
    app.run(host="0.0.0.0", port=settings.PORT)
