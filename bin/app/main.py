from flask import Flask
from flask import request
from loguru import logger

from chainik.pipelines.predict import response


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.get("data")
    return response(data=data)


@app.route("/result_question", methods=["POST"])
def result_question():
    data = request.form.get("data")

    #  data:
    #  {
    #
    #    'number of game': 5,
    #
    #    'question': "Что есть у Пескова?",
    #    'answer': 1,
    #
    #    'bank': 4000,
    #    'saved money': 1000,
    #    'response type': "good"
    #
    #  }

    #  data:
    #  {
    #
    #    'number of game': 5,
    #
    #    'question': "Что есть у Пескова?",
    #    'answer': 4,
    #
    #    'bank': 1000,
    #    'saved money': 1000,
    #    'response type': "bad"
    #
    #  }

    return {"data": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090)
