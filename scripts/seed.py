
"""
Seed script to populate sample data for Gradebook CLI.
Creates 3 students, 2 courses, enrollments, and grades.
"""

from gradebook import service

def main():
    print("🌱 Seeding sample data...")

    # Add students
    s1 = service.add_student("Elira Krasniqi")
    s2 = service.add_student("Ardit Gashi")
    s3 = service.add_student("Learta Morina")

    # Add courses
    service.add_course("CS101", "Intro to Python")
    service.add_course("MKT201", "Digital Marketing Basics")

    # Enroll students
    service.enroll(s1, "CS101")
    service.enroll(s1, "MKT201")
    service.enroll(s2, "CS101")
    service.enroll(s3, "MKT201")

    # Add grades
    service.add_grade(s1, "CS101", 93)
    service.add_grade(s1, "MKT201", 88)
    service.add_grade(s2, "CS101", 76)
    service.add_grade(s3, "MKT201", 91)

    print("✅ Sample data created successfully!")

if __name__ == "__main__":
    main()
