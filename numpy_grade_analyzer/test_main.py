import unittest

import numpy as np

from main import analyze_grades


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


if __name__ == "__main__":
    unittest.main()
