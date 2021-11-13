python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel && pip install -e .
# python -m deeppavlov install ru_odqa_infer_wiki
python ./bin/app/main.py
