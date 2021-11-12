import requests
from loguru import logger


if __name__ == "__main__":
    resp = requests.post(
        "http://127.0.0.1:8090/predict",
        data={
            "number of game": 5,
            "question": "Что есть у Пескова?",
            "answer_1": "Усы",
            "answer_2": "Борода",
            "answer_3": "Лысина",
            "answer_4": "Третья нога",
            "question money": 4000,
            "saved money": 1000,
            "available help": ["fifty fifty", "can mistake", "take money"],
        },
    )
    logger.info(resp.content)
