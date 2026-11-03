"""Analyze a small student gradebook using NumPy."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class GradeReport:
    student_averages: NDArray[np.float64]
    subject_averages: NDArray[np.float64]
    top_student: str
    passing_students: NDArray[np.str_]


def plot_report(
    student_names: NDArray[np.str_],
    subject_names: NDArray[np.str_],
    report: GradeReport,
    pass_mark: float,
    output_path: Path,
    show: bool = True,
) -> None:
    """Save charts of student and subject averages, optionally displaying them."""
    figure, (student_axis, subject_axis) = plt.subplots(1, 2, figsize=(11, 5))

    student_axis.bar(student_names, report.student_averages, color="steelblue")
    student_axis.axhline(
        pass_mark, color="tomato", linestyle="--", label=f"Pass mark ({pass_mark:g})"
    )
    student_axis.set_title("Average by student")
    student_axis.set_ylabel("Average score")
    student_axis.set_ylim(0, 100)
    student_axis.tick_params(axis="x", rotation=25)
    student_axis.legend()

    subject_axis.bar(subject_names, report.subject_averages, color="mediumseagreen")
    subject_axis.set_title("Average by subject")
    subject_axis.set_ylabel("Average score")
    subject_axis.set_ylim(0, 100)

    figure.suptitle("Grade Analysis")
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    if show:
        plt.show()
    plt.close(figure)


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
    parser.add_argument(
        "--plot-path",
        type=Path,
        default=Path("grade_report.png"),
        help="File path for the saved graph (default: grade_report.png).",
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
    plot_report(students, subjects, report, args.pass_mark, args.plot_path)
    print(f"\nGraph saved to: {args.plot_path}")


if __name__ == "__main__":
    main()
