import argparse
from gradebook.utils import setup_logging, parse_grade
from gradebook import service

def main(argv=None) -> int:
    setup_logging()
    parser = argparse.ArgumentParser(prog="gradebook", description="Gradebook CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("add-student")
    p1.add_argument("--name", required=True)

    p2 = sub.add_parser("add-course")
    p2.add_argument("--code", required=True)
    p2.add_argument("--title", required=True)

    p3 = sub.add_parser("enroll")
    p3.add_argument("--student-id", type=int, required=True)
    p3.add_argument("--course", required=True)

    p4 = sub.add_parser("add-grade")
    p4.add_argument("--student-id", type=int, required=True)
    p4.add_argument("--course", required=True)
    p4.add_argument("--grade", required=True)

    p5 = sub.add_parser("list")
    p5.add_argument("what", choices=["students", "courses", "enrollments"])
    p5.add_argument("--sort", choices=["name", "code", "title", "id"], default=None)

    p6 = sub.add_parser("avg")
    p6.add_argument("--student-id", type=int, required=True)
    p6.add_argument("--course", required=True)

    p7 = sub.add_parser("gpa")
    p7.add_argument("--student-id", type=int, required=True)

    args = parser.parse_args(argv)

    try:
        if args.cmd == "add-student":
            sid = service.add_student(args.name)
            print(f"✅ Added student #{sid}: {args.name}")

        elif args.cmd == "add-course":
            service.add_course(args.code, args.title)
            print(f"✅ Added course {args.code}: {args.title}")

        elif args.cmd == "enroll":
            service.enroll(args.student_id, args.course)
            print(f"✅ Enrolled student {args.student_id} to {args.course}")

        elif args.cmd == "add-grade":
            grade = parse_grade(args.grade)
            service.add_grade(args.student_id, args.course, grade)
            print(f"✅ Added grade {grade:.2f}")

        elif args.cmd == "list":
            if args.what == "students":
                for s in service.list_students(sort_by=(args.sort or "id")):
                    print(f"{s['id']:>3}  {s['name']}")
            elif args.what == "courses":
                for c in service.list_courses(sort_by=(args.sort or "code")):
                    print(f"{c['code']:<8} {c['title']}")
            else:
                # FIXED: show enrollments with names/titles
                students = {s["id"]: s["name"] for s in service.list_students()}
                courses = {c["code"]: c["title"] for c in service.list_courses()}
                for e in service.list_enrollments():
                    grades = ", ".join(f"{g:.1f}" for g in e.get("grades", [])) or "—"
                    student_name = students.get(e["student_id"], f"Student {e['student_id']}")
                    course_title = courses.get(e["course_code"], e["course_code"])
                    print(f"{student_name} [{e['student_id']}] -> {e['course_code']} {course_title} | grades: {grades}")

        elif args.cmd == "avg":
            avg = service.compute_average(args.student_id, args.course)
            print(f"📊 Average: {avg:.2f}")

        elif args.cmd == "gpa":
            gpa = service.compute_gpa(args.student_id)
            print(f"🎓 GPA: {gpa:.2f}")

    except ValueError as e:
        print("Error:", e)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
