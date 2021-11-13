import sys
from copy import deepcopy

import numpy as np
import pandas as pd
import requests
from loguru import logger

from vasserman import settings


def ask(number_of_game, row, i, saved_money, available_help, true_answer=None, ff=False, after_cm=0):
    request_data = {
        "number of game": number_of_game,
        "question": row["Вопрос"],
        "question money": settings.MONEY[i][0],
        "saved money": saved_money,
        "available help": available_help,
    }
    if ff:
        if not true_answer:
            # упрощение. оставляем правильный и случайный вариант
            request_data["answer_1"] = row["1"]
            request_data["answer_2"] = row["2"]
            request_data["answer_3"] = None
            request_data["answer_4"] = None
        else:
            for i in range(4):
                n = i + 1
                n_rand = [j for j in np.random.choice(4, size=2, replace=False) if j != true_answer][0]
                request_data[f"answer_{n}"] = row[f"{n}"] if n == true_answer or n == n_rand else ""

    else:
        request_data["answer_1"] = row["1"]
        request_data["answer_2"] = row["2"]
        request_data["answer_3"] = row["3"]
        request_data["answer_4"] = row["4"]
        if after_cm != 0:
            request_data["answer_{after_cm}"] = ""

    request_data["true"] = row["Правильный ответ"]

    return requests.post(
        f"{settings.SERVER_HOST}/predict", data=request_data
    ).json()  # {"answer" : int(row["Правильный ответ"])}


def check_answer(answer, row, i, saved_money, bank, number_of_game, cm=False):
    true_answer = int(float(row["Правильный ответ"]))
    new_saved_money = saved_money
    request_data = {
        "number of game": number_of_game,
        "question": row["Вопрос"],
        # "answer": true_answer,
        "answer": None if cm else true_answer,
    }

    if answer == true_answer:
        bank = settings.MONEY[i][0]
        if settings.MONEY[i][1]:
            new_saved_money = settings.MONEY[i][0]
        request_data["response type"] = "good"
        logger.debug(f"{row['Вопрос']} +++, success")
    elif cm:
        request_data["response type"] = "try again"
        logger.debug(f"{row['Вопрос'], *(row[f'{i+1}'] for i in range(4))} --- {answer} ({true_answer}) ---, retry")
    else:
        bank = saved_money
        request_data["response type"] = "bad"
        logger.info(f"{row['Вопрос'], *(row[f'{i+1}'] for i in range(4))} --- {answer} ({true_answer}) ---, FAIL")

    request_data["bank"] = bank
    request_data["saved money"] = new_saved_money

    requests.post(f"{settings.SERVER_HOST}/result_question", data=request_data).json()
    return bank, new_saved_money, answer == true_answer


def check(dataset: pd.DataFrame, level: str = "INFO"):
    np.random.seed(settings.RANDOM_STATE)
    logger.remove()
    logger.add(sys.stderr, level=level)

    n_samples = dataset.shape[0]
    n_stages = len(settings.MONEY)
    n_dropped = 0

    available_help = deepcopy(settings.AVAILABLE_HELP)
    saved_money = 0
    bank = 0
    total = 0
    number_of_game = 0
    N = n_samples / (n_stages + 1)  # one for "new question"

    logger.info(f"N of games = {N}\n")

    while number_of_game < N:
        for i in range(n_stages):
            idx = number_of_game * (n_stages + 1) + i
            row = dataset.iloc[idx]
            logger.debug(f"- question ({i+1}/{len(settings.MONEY)}) | game ({number_of_game + 1})")

            resp = ask(number_of_game, row, i, saved_money, available_help)
            if "end game" in resp:
                logger.debug("***END*** eng game")
                number_of_game += 1
                total += bank
                bank = 0
                saved_money = 0
                available_help = deepcopy(settings.AVAILABLE_HELP)
                logger.info(
                    f"\n\n--- game #{number_of_game} = {i + 1}/{n_stages} [bank = {total / 1e6}] "
                    f"\n--- game #{number_of_game + 1} started --- \n"
                )
                break

            elif "answer" in resp:
                if "help" in resp:
                    assert resp.get("help") == "can mistake"
                    assert "can mistake" in available_help
                    available_help.remove("can mistake")
                    logger.debug("///MISTAKE/// can mistake")
                    bank, saved_money, status = check_answer(
                        int(resp.get("answer", 0)), row, i, saved_money, bank, number_of_game, cm=True
                    )
                    if not status:
                        resp2 = ask(
                            number_of_game, row, i, saved_money, available_help, after_cm=int(resp.get("answer"))
                        )
                        bank, saved_money, status = check_answer(
                            int(resp2.get("answer", 0)), row, i, saved_money, bank, number_of_game
                        )
                else:
                    bank, saved_money, status = check_answer(
                        int(resp.get("answer", 0)), row, i, saved_money, bank, number_of_game
                    )

                # переход к следующей игре
                if not status:
                    number_of_game += 1
                    total += bank
                    bank = 0
                    saved_money = 0
                    available_help = deepcopy(settings.AVAILABLE_HELP)
                    logger.info(
                        f"\n\n--- game #{number_of_game} = {i}/{n_stages} [bank = {total / 1e6}] "
                        f"\n--- game #{number_of_game + 1} started --- \n"
                    )
                    break

            else:
                if resp.get("help") == "fifty fifty":
                    assert "fifty fifty" in available_help
                    available_help.remove("fifty fifty")
                    logger.debug("50////50 fifty fifty")
                    resp2 = ask(
                        number_of_game,
                        row,
                        i,
                        saved_money,
                        available_help,
                        ff=True,
                        true_answer=int(float(row["Правильный ответ"])),
                    )
                    bank, saved_money, _ = check_answer(
                        int(resp2.get("answer", 0)), row, i, saved_money, bank, number_of_game
                    )
                elif resp.get("help") == "new question":
                    assert "new question" in available_help
                    available_help.remove("new question")
                    logger.debug("///NEW/// new question")
                    row_new_question = dataset.iloc[(number_of_game + 1) * (n_stages + 1) - 1]
                    n_dropped += 1
                    resp2 = ask(number_of_game, row_new_question, i, saved_money, available_help)
                    bank, saved_money, _ = check_answer(
                        int(resp2.get("answer", 0)), row_new_question, i, saved_money, bank, number_of_game
                    )
                else:
                    logger.error("------------Bad output------------")
                    raise Exception

            if i == len(settings.MONEY) - 1:
                number_of_game += 1
                total += bank
                bank = 0
                saved_money = 0
                available_help = deepcopy(settings.AVAILABLE_HELP)
                logger.info(
                    f"\n\n--- game #{number_of_game} = {i + 1}/{n_stages} [bank = {total / 1e6}] "
                    f"\n--- game #{number_of_game + 1} started --- \n"
                )

    return bank
