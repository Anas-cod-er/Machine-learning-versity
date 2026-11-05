"""Analyze product and regional sales using NumPy."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class SalesReport:
    products: NDArray[np.str_]
    revenue_by_product: NDArray[np.float64]
    regions: NDArray[np.str_]
    revenue_by_region: NDArray[np.float64]
    total_revenue: float
    top_product: str


def read_sales_csv(
    csv_path: Path,
) -> tuple[NDArray[np.str_], NDArray[np.str_], NDArray[np.float64], NDArray[np.float64]]:
    """Read product, region, units_sold, and unit_price columns from a CSV."""
    required_columns = {"product", "region", "units_sold", "unit_price"}
    products: list[str] = []
    regions: list[str] = []
    units_sold: list[float] = []
    unit_prices: list[float] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must include these columns: product, region, units_sold, unit_price."
            )

        for row_number, row in enumerate(reader, start=2):
            product = (row.get("product") or "").strip()
            region = (row.get("region") or "").strip()
            if not product or not region:
                raise ValueError(f"CSV row {row_number} must have a product and region.")
            try:
                units = float(row["units_sold"])
                price = float(row["unit_price"])
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"CSV row {row_number} must contain numeric units_sold and unit_price."
                ) from error

            products.append(product)
            regions.append(region)
            units_sold.append(units)
            unit_prices.append(price)

    return (
        np.asarray(products, dtype=np.str_),
        np.asarray(regions, dtype=np.str_),
        np.asarray(units_sold, dtype=np.float64),
        np.asarray(unit_prices, dtype=np.float64),
    )


def analyze_sales(
    products: NDArray[np.str_],
    regions: NDArray[np.str_],
    units_sold: NDArray[np.float64],
    unit_prices: NDArray[np.float64],
) -> SalesReport:
    """Calculate revenue totals by product and region."""
    arrays = (products, regions, units_sold, unit_prices)
    if any(array.ndim != 1 for array in arrays):
        raise ValueError("Sales data must be one-dimensional.")
    if not products.size:
        raise ValueError("At least one sales record is required.")
    if any(array.size != products.size for array in arrays[1:]):
        raise ValueError("All sales columns must have the same number of records.")
    if any(not name.strip() for name in products) or any(
        not name.strip() for name in regions
    ):
        raise ValueError("Product and region names cannot be empty.")
    if (
        not np.isfinite(units_sold).all()
        or np.any(units_sold <= 0)
        or np.any(units_sold != np.floor(units_sold))
    ):
        raise ValueError("Units sold must be positive whole numbers.")
    if not np.isfinite(unit_prices).all() or np.any(unit_prices < 0):
        raise ValueError("Unit prices must be finite, non-negative numbers.")

    revenue = units_sold * unit_prices
    product_names, product_indices = np.unique(products, return_inverse=True)
    region_names, region_indices = np.unique(regions, return_inverse=True)
    product_revenue = np.bincount(product_indices, weights=revenue)
    region_revenue = np.bincount(region_indices, weights=revenue)

    return SalesReport(
        products=product_names,
        revenue_by_product=product_revenue,
        regions=region_names,
        revenue_by_region=region_revenue,
        total_revenue=float(revenue.sum()),
        top_product=str(product_names[int(np.argmax(product_revenue))]),
    )


def plot_report(report: SalesReport, output_path: Path, show: bool = True) -> None:
    """Save product and regional revenue charts, optionally displaying them."""
    figure, (product_axis, region_axis) = plt.subplots(1, 2, figsize=(11, 5))
    product_axis.bar(report.products, report.revenue_by_product, color="green")
    product_axis.set_title("Revenue by product")
    product_axis.set_ylabel("Revenue")
    product_axis.tick_params(axis="x", rotation=25)

    region_axis.bar(report.regions, report.revenue_by_region, color="green")
    region_axis.set_title("Revenue by region")
    region_axis.set_ylabel("Revenue")
    region_axis.tick_params(axis="x", rotation=25)

    figure.suptitle("Sales Analysis")
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    if show:
        plt.show()
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze sales from a CSV file.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).with_name("sample_sales.csv"),
        help="CSV file to analyze (default: sample_sales.csv).",
    )
    parser.add_argument(
        "--plot-path",
        type=Path,
        default=Path("sales_report.png"),
        help="File path for the saved graph (default: sales_report.png).",
    )
    args = parser.parse_args()

    try:
        products, regions, units_sold, unit_prices = read_sales_csv(args.csv)
        report = analyze_sales(products, regions, units_sold, unit_prices)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print("Revenue by product:")
    for product, revenue in zip(report.products, report.revenue_by_product):
        print(f"  {product}: ${revenue:,.2f}")

    print("\nRevenue by region:")
    for region, revenue in zip(report.regions, report.revenue_by_region):
        print(f"  {region}: ${revenue:,.2f}")

    print(f"\nTotal revenue: ${report.total_revenue:,.2f}")
    print(f"Top product by revenue: {report.top_product}")
    plot_report(report, args.plot_path)
    print(f"Graph saved to: {args.plot_path}")


if __name__ == "__main__":
    main()
