
### Development Set Up

Set up of the development environment for the animation modules for future reference.

To set up and acitvate the virtual environment for this project, run following commands on your cmd inside the project folder:

### Windows

**Note: working Python, npm and Node.js installation required**

_make virtual environment:_
```
python -m venv venv
```

_activate environment:_
Note: this is not necessary to run the Jupyter Notebooks, but to install the requirements.
```
.\venv\Scripts\activate
```

_install requirements inside venv:_
```
pip install -r requirements.txt
```

_install ipympl for matplotlib widgets:_
```
pip install notebook ipympl matplotlib
```

_activate pre commit hooks:_
```
pre-commit install
```
