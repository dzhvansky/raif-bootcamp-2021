import typing

from vasserman import settings
from vasserman.models.questions import QuestionProcessor

QUESTION_PROC = None


def load_question_proc() -> None:
    """
    Function to load the first processing stage.
    Parameters from settings are used.
    Returns: None
    """
    global QUESTION_PROC
    if QUESTION_PROC is None:
        QUESTION_PROC = QuestionProcessor(ft_model_path=settings.FT_MODEL_PATH)


def response(data) -> typing.Dict[str, typing.Union[int, str]]:
    load_question_proc()
    return QUESTION_PROC.answer(request=data)
