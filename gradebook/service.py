from __future__ import annotations
from typing import Dict, Any, List, Optional
from statistics import mean
from .storage import load_data, save_data
from .models import Student, Course, Enrollment

def _next_id(items: List[Dict[str, Any]]): return (max((i["id"] for i in items), default=-1) + 1)

def add_student(name, *, path=None):
    data = load_data(path)
    sid = _next_id(data["students"])
    data["students"].append({"id": sid, "name": name})
    save_data(data, path)
    return sid

def add_course(code, title, *, path=None):
    data = load_data(path)
    data["courses"].append({"code": code, "title": title})
    save_data(data, path)

def enroll(student_id, course_code, *, path=None):
    data = load_data(path)
    data["enrollments"].append({"student_id": student_id, "course_code": course_code, "grades": []})
    save_data(data, path)

def add_grade(student_id, course_code, grade, *, path=None):
    data = load_data(path)
    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            e["grades"].append(grade)
            save_data(data, path)
            return
    raise ValueError("Enrollment not found")

def list_students(sort_by=None, *, path=None):
    data = load_data(path)
    students = data["students"]
    if sort_by:
        students = sorted(students, key=lambda s: s.get(sort_by))
    return students


def list_courses(sort_by=None, *, path=None):
    data = load_data(path)
    courses = data["courses"]
    if sort_by:
        courses = sorted(courses, key=lambda c: c.get(sort_by))
    return courses


def list_enrollments(*, path=None):
    return load_data(path)["enrollments"]

def compute_average(student_id, course_code, *, path=None):
    data = load_data(path)
    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            if not e["grades"]: raise ValueError("No grades yet.")
            return mean(e["grades"])
    raise ValueError("Enrollment not found")

def compute_gpa(student_id, *, path=None):
    data = load_data(path)
    avgs = [mean(e["grades"]) for e in data["enrollments"] if e["student_id"] == student_id and e["grades"]]
    if not avgs: raise ValueError("No grades yet.")
    return mean(avgs)
