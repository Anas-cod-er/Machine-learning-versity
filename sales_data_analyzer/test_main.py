from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np

from main import analyze_sales, plot_report, read_sales_csv


class AnalyzeSalesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.products = np.array(["Pen", "Book", "Pen"])
        self.regions = np.array(["North", "South", "South"])
        self.units_sold = np.array([10, 4, 5], dtype=np.float64)
        self.unit_prices = np.array([2.5, 12, 2.5], dtype=np.float64)

    def test_calculates_revenue_totals_and_top_product(self) -> None:
        report = analyze_sales(
            self.products, self.regions, self.units_sold, self.unit_prices
        )

        np.testing.assert_array_equal(report.products, ["Book", "Pen"])
        np.testing.assert_allclose(report.revenue_by_product, [48, 37.5])
        np.testing.assert_array_equal(report.regions, ["North", "South"])
        np.testing.assert_allclose(report.revenue_by_region, [25, 60.5])
        self.assertEqual(report.total_revenue, 85.5)
        self.assertEqual(report.top_product, "Book")

    def test_rejects_mismatched_column_lengths(self) -> None:
        with self.assertRaisesRegex(ValueError, "same number of records"):
            analyze_sales(
                self.products, self.regions, self.units_sold[:-1], self.unit_prices
            )

    def test_rejects_fractional_units(self) -> None:
        units_sold = self.units_sold.copy()
        units_sold[0] = 1.5

        with self.assertRaisesRegex(ValueError, "positive whole numbers"):
            analyze_sales(self.products, self.regions, units_sold, self.unit_prices)

    def test_rejects_negative_price(self) -> None:
        prices = self.unit_prices.copy()
        prices[0] = -1

        with self.assertRaisesRegex(ValueError, "non-negative"):
            analyze_sales(self.products, self.regions, self.units_sold, prices)

    def test_reads_csv_records(self) -> None:
        with TemporaryDirectory() as directory:
            csv_path = Path(directory) / "sales.csv"
            csv_path.write_text(
                "product,region,units_sold,unit_price\nPen,North,10,2.5\n",
                encoding="utf-8",
            )

            products, regions, units, prices = read_sales_csv(csv_path)

        np.testing.assert_array_equal(products, ["Pen"])
        np.testing.assert_array_equal(regions, ["North"])
        np.testing.assert_allclose(units, [10])
        np.testing.assert_allclose(prices, [2.5])

    def test_saves_sales_chart(self) -> None:
        report = analyze_sales(
            self.products, self.regions, self.units_sold, self.unit_prices
        )

        with TemporaryDirectory() as directory:
            output_path = Path(directory) / "sales_report.png"
            plot_report(report, output_path, show=False)

            self.assertTrue(output_path.is_file())
            self.assertGreater(output_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
