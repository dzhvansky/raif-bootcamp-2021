import typing

# import fasttext
import numpy as np
from loguru import logger
from scipy.spatial import distance


class QuestionProcessor:
    def __init__(self, ft_model_path, **params):
        self.params = params
        self.model_path = ft_model_path
        # self.ft_model = fasttext.FastText.load_model(ft_model_path)

    def _get_ft_scores(self, question: str, answers: typing.List[str]) -> np.array:
        # question_vec = self.ft_model.get_sentence_vector(question)
        # scores = np.zeros(4)
        # for i, answer in enumerate(answers):
        #     if " " in answer:
        #         scores[i] = distance.cosine(question_vec, self.ft_model.get_sentence_vector(answer))
        #     else:
        #         scores[i] = distance.cosine(question_vec, self.ft_model.get_word_vector(answer))
        return [2,3,1,0]

    def answer(self, request: typing.Dict) -> typing.Dict:
        scores = self._get_ft_scores(request["question"], [request[f"answer_{i+1}"] for i in range(4)])
        logger.info(f"scores = {scores}")
        return {"answer": 1 + np.argmax(scores).item()}

    #  data:
    #  {
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
    #  }

    #  resp:
    #  {
    #    'help': "fifty fifty",
    #  }

    #  resp:
    #  {
    #    'help': "can mistake",
    #    'answer': 1,
    #  }

    #  resp:
    #  {
    #    'end game': "take money",
    #  }