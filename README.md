
## Installation
---

### Install Python

https://www.python.org/downloads/windows/

### Virtualenv
```
pip install virtualenv
```

Create a new env (ONLY IF NOT CREATED)
```
python -m venv ./venv
```

Activate virtualvenv
```
./venv/Scripts/activate
```

### Install pip dependency 
```
pip install -r requirements.txt
```

## Run the app

Run flask app
```
$env:FLASK_ENV = "development"
python -m flask run
```

or 

```
./run.bash
```
