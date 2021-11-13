import typing
from pathlib import Path


PROJ_DIR: Path = Path(__file__).parent.parent
MODEL_DIR: Path = PROJ_DIR.joinpath("data", "models")
FT_MODEL_PATH: str = str(MODEL_DIR.joinpath("wiki-ru.bin").resolve())

RANDOM_STATE: int = 42

MONEY: typing.List[typing.Tuple[int, bool]] = [
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

QUESTIONS: typing.Dict[str, int] = {str(m[0]): i for i, m in enumerate(MONEY)}

AVAILABLE_HELP: typing.List[str] = ["fifty fifty", "can mistake", "new question"]

DUMMY_DATA_SAMPLE: typing.Dict = {
    "number of game": 0,
    "question": "Вопрос",
    "question money": 100,
    "answer_1": "?",
    "answer_2": "?",
    "answer_3": "?",
    "answer_4": "?",
    "saved money": 0,
    "available help": AVAILABLE_HELP,
}

PORT: int = 8090
SERVER_HOST: str = f"http://192.168.1.68:{PORT}"
