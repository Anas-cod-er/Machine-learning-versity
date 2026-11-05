# NumPy Sales Data Analyzer

A beginner-friendly project that reads sales records from CSV and uses NumPy
to calculate revenue by product and region, total revenue, and the top product
by revenue. It also saves a chart as `sales_report.png`.

The CSV must contain `product`, `region`, `units_sold`, and `unit_price`
columns. Units sold must be positive whole numbers; prices must be
non-negative.

## Run

From this directory:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Analyze a different CSV or choose a different chart path:

```powershell
python main.py --csv data\quarterly_sales.csv --plot-path results\quarterly.png
```

## Tests

```powershell
python -m unittest -v
```
