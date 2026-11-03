from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np

from main import analyze_grades, plot_report


class AnalyzeGradesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.students = np.array(["Amina", "Bilal", "Chloe"])
        self.subjects = np.array(["Math", "Science"])
        self.grades = np.array(
            [[80, 90], [50, 60], [100, 90]],
            dtype=np.float64,
        )

    def test_calculates_averages_and_identifies_students(self) -> None:
        report = analyze_grades(self.students, self.subjects, self.grades)

        np.testing.assert_allclose(report.student_averages, [85, 55, 95])
        np.testing.assert_allclose(report.subject_averages, [230 / 3, 80])
        self.assertEqual(report.top_student, "Chloe")
        np.testing.assert_array_equal(report.passing_students, ["Amina", "Chloe"])

    def test_uses_custom_pass_mark(self) -> None:
        report = analyze_grades(self.students, self.subjects, self.grades, 90)

        np.testing.assert_array_equal(report.passing_students, ["Chloe"])

    def test_rejects_mismatched_grade_dimensions(self) -> None:
        with self.assertRaisesRegex(ValueError, "one row per student"):
            analyze_grades(self.students, self.subjects, self.grades[:, :1])

    def test_rejects_invalid_grade(self) -> None:
        grades = self.grades.copy()
        grades[0, 0] = 101

        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            analyze_grades(self.students, self.subjects, grades)

    def test_saves_average_graph(self) -> None:
        report = analyze_grades(self.students, self.subjects, self.grades)

        with TemporaryDirectory() as directory:
            output_path = Path(directory) / "grade_report.png"
            plot_report(self.students, self.subjects, report, 60, output_path, show=False)

            self.assertTrue(output_path.is_file())
            self.assertGreater(output_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
