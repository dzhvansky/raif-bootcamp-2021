import json
import typing

from loguru import logger


def response(data) -> typing.Dict[str, typing.Union[int, str]]:
    logger.debug(data)

    #  data:
    #  {
    #
    #    'number of game': 5,
    #
    #    'question': "Что есть у Пескова?",
    #    'answer_1': "Усы",
    #    'answer_2': "Борода",
    #    'answer_3': "Лысина",
    #    'answer_4': "Третья нога",
    #
    #    'question money': 4000,
    #    'saved money': 1000,
    #    'available help': ["fifty fifty", "can mistake", "take money"]
    #
    #  }

    #  resp:
    #  {
    #
    #    'help': "fifty fifty",
    #
    #  }

    #  resp:
    #  {
    #
    #    'help': "can mistake",
    #    'answer': 1,
    #
    #  }

    #  resp:
    #  {
    #
    #    'end game': "take money",
    #
    #  }
    return {"answer": int(data.get("number of game", 0)) % 4 + 1}



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