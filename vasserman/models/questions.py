import typing

import re

# import fasttext
import numpy as np

# from loguru import logger
# from scipy.spatial import distance
from scipy.special import softmax

from vasserman import settings

THRESHOLDS = np.array(
    [
        # минимальный, уверенный, подсказка50/50, подсказкаправо
        [0.05, 0.7, 0.2, 0.3],  # 1
        [0.21, 0.75, 0.3, 0.4],  # 2
        [0.21, 0.75, 0.3, 0.4],  # 3
        [0.209, 0.75, 0.3, 0.4],  # 4
        [0.2, 0.8, 0.3, 0.4],  # 5
        [0.2, 0.85, 0.25, 0.3],  # 6
        [0.2, 0.9, 0.3, 0.4],  # 7
        [0.206, 0.85, 0.3, 0.4],  # 8
        [0.207, 0.614, 0.3, 0.4],  # 9
        [0.208, 0.615, 0.3, 0.4],  # 10
        [0.1, 0.4, 0.25, 0.3],  # 11
        [0.22, 0.63, 0.3, 0.4],  # 12
        [0.24, 0.69, 0.3, 0.4],  # 13
        [0.3, 0.81, 0.4, 0.5],  # 14
        [0.4, 0.9, 0.4, 0.5],  # 15
    ]
)


class QuestionProcessor:
    def __init__(self, ft_model_path, **params):
        self.params = params
        self.model_path = ft_model_path
        self.previous_response = {}
        # self.ft_model = fasttext.FastText.load_model(ft_model_path)

    def _get_probs(
        self, question: str, answers: typing.List[str], true_answer: typing.Optional[str] = None
    ) -> np.array:
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

        q_idx = settings.QUESTIONS[request["question money"]]

        if self.previous_response and q_idx == self.previous_response.get("q_idx"):
            probs = self.previous_response["probs"]
            if self.previous_response["help"] == "can mistake":
                probs[self.previous_response["answer"] - 1] = 0
            else:
                assert self.previous_response["help"] == "fifty fifty"
                probs[[i for i in range(4) if request[f"answer_{i+1}"] == ""]] = 0

            probs = probs / probs.sum()

        else:
            probs = self._get_probs(
                request["question"], [request[f"answer_{i + 1}"] for i in range(4)], true_answer=request.get("true")
            )

        # check for wrong answer
        probs[[i for i in range(4) if re.findall(r"неверный\s+ответ", request[f"answer_{i+1}"].lower())]] = 0
        probs = probs / probs.sum()

        prob = np.max(probs).item()
        # answer = 1 + np.random.choice(range(4), p=probs).item()  # np.argmax(probs).item()
        answer = 1 + np.argmax(probs).item()

        if prob > THRESHOLDS[q_idx, 1]:
            self.previous_response = {}
            return {"answer": answer}
        elif (
            prob > THRESHOLDS[q_idx, 3] and prob <= THRESHOLDS[q_idx, 1] and "can mistake" in request["available help"]
        ):
            output = {"help": "can mistake", "answer": answer}
            self.previous_response = {
                "q_idx": q_idx,
                "probs": probs,
            }
            self.previous_response.update(output)
            return output
        elif (
            prob > THRESHOLDS[q_idx, 2] and prob <= THRESHOLDS[q_idx, 1] and "fifty fifty" in request["available help"]
        ):
            output = {"help": "fifty fifty"}
            self.previous_response = {
                "q_idx": q_idx,
                "probs": probs,
            }
            self.previous_response.update(output)
            return output
        else:
            self.previous_response = {}
            return {"end game": "take money"}

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
