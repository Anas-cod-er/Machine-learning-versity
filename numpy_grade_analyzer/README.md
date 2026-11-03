# NumPy Grade Analyzer

A small, beginner-friendly project that uses NumPy to analyze student grades.
It calculates each student's average, each subject's average, identifies the
top student, and lists students who meet the pass mark.

## Run

From this directory:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Set a different pass mark with:

```powershell
python main.py --pass-mark 75
```

## Tests

```powershell
python -m unittest -v
```

The sample gradebook and tests use NumPy arrays; averages and filtering are
computed with NumPy operations.
