"""Analyze a small student gradebook using NumPy."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class GradeReport:
    student_averages: NDArray[np.float64]
    subject_averages: NDArray[np.float64]
    top_student: str
    passing_students: NDArray[np.str_]


def analyze_grades(
    student_names: NDArray[np.str_],
    subject_names: NDArray[np.str_],
    grades: NDArray[np.float64],
    pass_mark: float = 60.0,
) -> GradeReport:
    """Calculate average scores and identify top and passing students."""
    if student_names.ndim != 1 or subject_names.ndim != 1:
        raise ValueError("Student and subject names must be one-dimensional.")
    if grades.shape != (student_names.size, subject_names.size):
        raise ValueError("Grades must have one row per student and one column per subject.")
    if student_names.size == 0 or subject_names.size == 0:
        raise ValueError("At least one student and one subject are required.")
    if not np.isfinite(grades).all() or np.any((grades < 0) | (grades > 100)):
        raise ValueError("Grades must be finite numbers between 0 and 100.")
    if not np.isfinite(pass_mark) or not 0 <= pass_mark <= 100:
        raise ValueError("The pass mark must be between 0 and 100.")

    student_averages = grades.mean(axis=1)
    subject_averages = grades.mean(axis=0)
    passing_students = student_names[student_averages >= pass_mark]

    return GradeReport(
        student_averages=student_averages,
        subject_averages=subject_averages,
        top_student=str(student_names[int(np.argmax(student_averages))]),
        passing_students=passing_students,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a sample student gradebook.")
    parser.add_argument(
        "--pass-mark",
        type=float,
        default=60.0,
        help="Minimum student average required to pass (default: 60).",
    )
    args = parser.parse_args()

    students = np.array(["Amina", "Bilal", "Chloe", "David"])
    subjects = np.array(["Math", "Science", "English"])
    grades = np.array(
        [
            [88, 92, 85],
            [72, 65, 78],
            [95, 91, 94],
            [54, 61, 58],
        ],
        dtype=np.float64,
    )
    report = analyze_grades(students, subjects, grades, args.pass_mark)

    print("Student averages:")
    for student, average in zip(students, report.student_averages):
        print(f"  {student}: {average:.1f}")

    print("\nSubject averages:")
    for subject, average in zip(subjects, report.subject_averages):
        print(f"  {subject}: {average:.1f}")

    print(f"\nTop student: {report.top_student}")
    print(
        f"Passing students ({report.passing_students.size}): "
        f"{', '.join(report.passing_students.tolist()) or 'None'}"
    )


if __name__ == "__main__":
    main()
