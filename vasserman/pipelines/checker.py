import json
from copy import deepcopy

import pandas as pd
import requests
from loguru import logger

MONEY = [
    (100, False),
    (200, False),
    (300, False),
    (500, False),
    (1000, True),
    (2000, False),
    (4000, False),
    (8000, False),
    (16000, False),
    (32000, True),
    (64000, False),
    (125000, False),
    (250000, False),
    (500000, False),
    (1000000, False),
]

NUMBER_OF_GAME = 1
AVAILABLE_HELP = ["fifty fifty", "can mistake", "new question"]
BANK = 0
SAVED_MONEY = 0

# SERVER_HOST = "http://192.168.1.68:8090"
SERVER_HOST = "http://localhost:8090"


def ask(number_of_game, row, i, saved_money, available_help, ff=False, after_cm=0):
    request_data = {
        "number of game": number_of_game,
        "question": row["Вопрос"],
        "question money": MONEY[i][0],
        "saved money": saved_money,
        "available help": available_help,
    }
    if ff:
        # упрощение. оставляем правильный и случайный вариант
        request_data["answer_1"] = row["1"]
        request_data["answer_2"] = row["2"]
        request_data["answer_3"] = None
        request_data["answer_4"] = None
    else:
        request_data["answer_1"] = row["1"]
        request_data["answer_2"] = row["2"]
        request_data["answer_3"] = row["3"]
        request_data["answer_4"] = row["4"]
        if after_cm != 0:
            request_data["answer_{after_cm}"] = None

    return requests.post(f"{SERVER_HOST}/predict", data=request_data).json()


def check_answer(answer, row, i, saved_money, bank, cm=False):
    new_saved_money = saved_money
    request_data = {
        "number of game": NUMBER_OF_GAME,
        "question": row["Вопрос"],
        "answer": None if cm else int(row["Правильный ответ"]),
    }

    if answer == int(row["Правильный ответ"]):
        bank = MONEY[i][0]
        if MONEY[i][1]:
            new_saved_money = MONEY[i][0]
        request_data["response type"] = "good"
    elif cm:
        request_data["response type"] = "try again"
    else:
        bank = saved_money
        request_data["response type"] = "bad"

    request_data["bank"] = bank
    request_data["saved money"] = new_saved_money

    requests.post(f"{SERVER_HOST}/result_question", data=request_data).json()
    return bank, new_saved_money, answer == int(row["Правильный ответ"])


def check(dataset: pd.DataFrame):
    available_help = deepcopy(AVAILABLE_HELP)
    saved_money = deepcopy(SAVED_MONEY)
    bank = deepcopy(BANK)
    for i, row in enumerate(dataset.iterrows()):
        resp = ask(NUMBER_OF_GAME, row[1], i, saved_money, available_help)
        if "end game" in resp:
            break
        elif "answer" in resp:
            if "help" in resp:
                assert resp.get("help") == "can mistake"
                assert "can mistake" in available_help
                available_help.remove("can mistake")
                bank, saved_money, status = check_answer(int(resp.get("answer")), row[1], i, saved_money, bank, cm=True)
                if not status:
                    resp2 = ask(
                        NUMBER_OF_GAME, row[1], i, saved_money, available_help, after_cm=int(resp.get("answer"))
                    )
                    bank, saved_money, _ = check_answer(int(resp2.get("answer")), row[1], i, saved_money, bank)
            else:
                bank, saved_money, _ = check_answer(int(resp.get("answer")), row[1], i, saved_money, bank)
        else:
            if resp.get("help") == "fifty fifty":
                assert "fifty fifty" in available_help
                available_help.remove("fifty fifty")
                resp2 = ask(NUMBER_OF_GAME, row[1], i, saved_money, available_help, ff=True)
                bank, saved_money = check_answer(int(resp2.get("answer")), row[1], i, saved_money, bank)
            elif resp.get("help") == "new question":
                assert "new question" in available_help
                available_help.remove("new question")
                row_new_question = row[1]
                resp2 = ask(NUMBER_OF_GAME, row_new_question, i, saved_money, available_help)
                bank, saved_money = check_answer(int(resp2.get("answer")), row_new_question, i, saved_money, bank)
            else:
                raise Exception

    print(bank)
