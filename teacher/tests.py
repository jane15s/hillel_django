from django.test import TestCase, Client
from django.contrib.auth.models import User
from common_data.models import Grade, Lesson


class TeacherEndpointsTests(TestCase):
    fixtures = ['fixture1.json']

    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.get(pk=4)
        self.client.force_login(self.teacher)

    def test_lessons_list_view(self):
        response = self.client.get(f'/teacher/{self.teacher.id}/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lessons")

    def test_lessons_list_forbidden_if_not_teacher(self):
        student = User.objects.get(pk=2)
        self.client.force_login(student)
        response = self.client.get(f'/teacher/{self.teacher.id}/lessons/')
        self.assertEqual(response.status_code, 403)

    def test_lessons_list_wrong_teacher_id(self):
        response = self.client.get('/teacher/999/lessons/')
        self.assertEqual(response.status_code, 404)

    def test_create_lesson(self):
        data = {
            "name": "New lesson",
            "description": "desc",
            "date": "2025-12-01",
            "room": "101",
            "homework": "read",
            "sclass_id": 1
        }
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/', data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Lesson.objects.filter(name="New lesson").exists())

    def test_create_lesson_forbidden_if_not_teacher(self):
        student = User.objects.get(pk=2)
        self.client.force_login(student)
        data = {
            "name": "X",
            "description": "Y",
            "date": "2025-12-01",
            "room": "1",
            "homework": "a",
            "sclass_id": 1
        }
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/', data)
        self.assertEqual(response.status_code, 403)

    def test_create_lesson_missing_fields(self):
        data = {"name": "X"}
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/', data)
        self.assertEqual(response.status_code, 400)

    def test_create_lesson_wrong_teacher_id(self):
        data = {
            "name": "X",
            "description": "Y",
            "date": "2025-12-01",
            "room": "1",
            "homework": "a",
            "sclass_id": 1
        }
        response = self.client.post('/teacher/999/lessons/', data)
        self.assertEqual(response.status_code, 404)

    def test_set_grade(self):
        data = {"student_id": 2, "grade": 11, "homework_grade": 10}
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/1/set_grade/', data)
        self.assertEqual(response.status_code, 302)
        grade = Grade.objects.get(student_id=2, lesson_id=1)
        self.assertEqual(grade.grade, 11)
        self.assertEqual(grade.homework_grade, 10)

    def test_set_grade_creates_if_missing(self):
        data = {"student_id": 1, "grade": 8, "homework_grade": 7}
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/1/set_grade/', data)
        self.assertEqual(response.status_code, 302)
        grade = Grade.objects.get(student_id=1, lesson_id=1)
        self.assertEqual(grade.grade, 8)
        self.assertEqual(grade.homework_grade, 7)

    def test_set_grade_forbidden_if_not_teacher(self):
        student = User.objects.get(pk=2)
        self.client.force_login(student)
        data = {"student_id": 2, "grade": 10, "homework_grade": 10}
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/1/set_grade/', data)
        self.assertEqual(response.status_code, 403)

    def test_set_grade_invalid_student(self):
        data = {"student_id": 999, "grade": 10, "homework_grade": 10}
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/1/set_grade/', data)
        self.assertEqual(response.status_code, 404)

    def test_set_grade_invalid_lesson(self):
        data = {"student_id": 2, "grade": 10, "homework_grade": 10}
        response = self.client.post(f'/teacher/{self.teacher.id}/lessons/999/set_grade/', data)
        self.assertEqual(response.status_code, 404)

