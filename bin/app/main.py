from flask import Flask
from flask import request

from vasserman.pipelines.predict import response

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    return response(data=request.form)


@app.route("/result_question", methods=["POST"])
def result_question():
    _ = request.form
    return {"data": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
