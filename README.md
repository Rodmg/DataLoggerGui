# LoggerGui

GUI for PSoC Logger

# Use
- Enable virtualenv
```
source bin/activate
```

- Install dependencies
```
pip install -r requirements.txt
```

- Run
```
python app.py
```

# if matplotlib install fails: workaround

ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install matplotlib