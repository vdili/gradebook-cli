from typing import List
from dataclasses import dataclass, field

def _require_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")
    return value.strip()

def _require_id_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer.")
    return value

def _validate_grade(g: float) -> float:
    g = float(g)
    if not (0 <= g <= 100):
        raise ValueError("grade must be between 0 and 100.")
    return g

@dataclass
class Student:
    id: int
    name: str
    def __post_init__(self):
        self.id = _require_id_int(self.id, "Student.id")
        self.name = _require_non_empty_str(self.name, "Student.name")
    def __str__(self): return f"Student(id={self.id}, name='{self.name}')"

@dataclass
class Course:
    code: str
    title: str
    def __post_init__(self):
        self.code = _require_non_empty_str(self.code, "Course.code")
        self.title = _require_non_empty_str(self.title, "Course.title")
    def __str__(self): return f"Course(code='{self.code}', title='{self.title}')"

@dataclass
class Enrollment:
    student_id: int
    course_code: str
    grades: List[float] = field(default_factory=list)
    def __post_init__(self):
        self.student_id = _require_id_int(self.student_id, "Enrollment.student_id")
        self.course_code = _require_non_empty_str(self.course_code, "Enrollment.course_code")
        self.grades = [_validate_grade(g) for g in self.grades]
    def add_grade(self, grade: float):
        self.grades.append(_validate_grade(grade))
