
import unittest, os, tempfile
from gradebook import service
from gradebook.storage import save_data

class ServiceTests(unittest.TestCase):
    def setUp(self):

        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "gb.json")
        save_data({"students": [], "courses": [], "enrollments": []}, self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_student(self):
        sid = service.add_student("Alice", path=self.path)
        students = service.list_students(path=self.path)
        self.assertEqual(students[0]["id"], sid)
        self.assertEqual(students[0]["name"], "Alice")

    def test_add_grade_and_average(self):
        s = service.add_student("Bob", path=self.path)
        service.add_course("CS101", "Intro", path=self.path)
        service.enroll(s, "CS101", path=self.path)
        service.add_grade(s, "CS101", 80, path=self.path)
        service.add_grade(s, "CS101", 90, path=self.path)
        avg = service.compute_average(s, "CS101", path=self.path)
        self.assertAlmostEqual(avg, 85.0)

    def test_add_grade_without_enrollment_raises(self):
        s = service.add_student("Cara", path=self.path)
        service.add_course("MATH1", "Math", path=self.path)
        with self.assertRaises(ValueError):
            service.add_grade(s, "MATH1", 70, path=self.path)

if __name__ == "__main__":
    unittest.main()
