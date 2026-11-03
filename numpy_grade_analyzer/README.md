# NumPy Grade Analyzer

A small, beginner-friendly project that uses NumPy to analyze student grades.
It calculates each student's average, each subject's average, identifies the
top student, and lists students who meet the pass mark. It also displays a
graph of student and subject averages and saves it as `grade_report.png`.

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

Choose a different file for the graph with:

```powershell
python main.py --plot-path results\grades.png
```

## Tests

```powershell
python -m unittest -v
```

The sample gradebook and tests use NumPy arrays; averages and filtering are
computed with NumPy operations, and Matplotlib draws the graph.
