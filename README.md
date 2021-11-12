# Bootcamp 2021 - team Chainik


python3.7 required
```
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -e . # pip install -r requirements_dev.txt

python -m ipykernel install --user --name bootcamp_py37

docker build --no-cache --tag local_vasserman:latest ./
docker run -it --name vasserman -p 8090:8090 local_vasserman
```

