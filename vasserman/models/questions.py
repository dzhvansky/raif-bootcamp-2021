import typing

# import fasttext
import numpy as np
from loguru import logger
from scipy.spatial import distance
from scipy.special import softmax

from vasserman import settings

THRESHOLDS = np.array([
                      #минимальный, уверенный, подсказка50/50, подсказкаправо
                      [0.05,0.4,0.2,0.3],#1
                      [0.21,0.62,0.3,0.4],#2
                      [0.21,0.62,0.3,0.4],#3
                      [0.209,0.618,0.3,0.4],#4
                      [0.2,0.6,0.3,0.4],#5
                      [0.2,0.6,0.25,0.3],#6
                      [0.2,0.6,0.3,0.4],#7
                      [0.206,0.612,0.3,0.4],#8
                      [0.207,0.614,0.3,0.4],#9
                      [0.208,0.615,0.3,0.4],#10
                      [0.1,0.4,0.25,0.3],#11
                      [0.22,0.63,0.3,0.4],#12
                      [0.24,0.69,0.3,0.4],#13
                      [0.3,0.81,0.4,0.5],#14
                      [0.4,0.9,0.4,0.5]#15
])


class QuestionProcessor:
    def __init__(self, ft_model_path, **params):
        self.params = params
        self.model_path = ft_model_path
        # self.ft_model = fasttext.FastText.load_model(ft_model_path)

    def _get_probs(self, question: str, answers: typing.List[str], true_answer: typing.Optional[str]=None) -> np.array:
        # question_vec = self.ft_model.get_sentence_vector(question)
        # scores = np.zeros(4)
        # for i, answer in enumerate(answers):
        #     if " " in answer:
        #         scores[i] = distance.cosine(question_vec, self.ft_model.get_sentence_vector(answer))
        #     else:
        #         scores[i] = distance.cosine(question_vec, self.ft_model.get_word_vector(answer))
        if not true_answer:
            true_answer = np.random.choice(4) + 1
        else:
            true_answer = int(float(true_answer))
        probs = softmax(np.random.randn(4))
        return np.roll(probs, true_answer - 1 - np.argmax(probs))

    def answer(self, request: typing.Dict) -> typing.Dict:
        probs = self._get_probs(request["question"], [request[f"answer_{i+1}"] for i in range(4)], true_answer=request.get("true"))
        # logger.info(f"probs = {probs}")
        prob = np.max(probs).item()
        answer = 1 + np.random.choice(range(4), p=probs).item() #np.argmax(probs).item()

        q_idx = settings.QUESTIONS[request['question money']]
        if prob > THRESHOLDS[q_idx, 1]:
            return {'answer': answer}
        elif prob > THRESHOLDS[q_idx, 3] and prob <= THRESHOLDS[q_idx, 1] and "can mistake" in request['available help']:
            return {'help': "can mistake", 'answer': answer}
        elif prob > THRESHOLDS[q_idx, 2] and prob <= THRESHOLDS[q_idx, 1] and "fifty fifty" in request['available help']:
            return {'help': "fifty fifty"}
        else:
            return {'end game': "take money"}

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