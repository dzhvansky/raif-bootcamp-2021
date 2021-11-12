python3.7 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -e .
python ./bin/app/main.py &
