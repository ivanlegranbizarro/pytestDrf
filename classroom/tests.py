import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from .models import Classroom, Student

pytestmark = pytest.mark.django_db


@pytest.fixture
def student1():
    return Student.objects.create(
        first_name="John",
        last_name="Doe",
        age=20,
        admission_number=1234,
        is_qualified=True,
        average_score=90,
    )


@pytest.fixture
def classroom1():
    return Classroom.objects.create(name="Class 1", student_capacity=10)


@pytest.fixture
def url_list_classrooms():
    return reverse("classroom:classroom-list")


@pytest.fixture
def url_retrieve_update_destroy_classroom(classroom1):
    return reverse("classroom:classroom-detail", kwargs={"pk": classroom1.id})


@pytest.fixture
def url_students_list():
    return reverse("classroom:students-list")


@pytest.fixture
def url_retrieve_update_destroy_student(student1):
    return reverse("classroom:student-detail", kwargs={"pk": student1.id})


@pytest.fixture
def user_token():
    user = User.objects.create_user(username="testuser", password="12345")
    token = Token.objects.create(user=user)
    return token.key


class TestStudentModel:
    def test_student_can_be_created(self, student1):
        assert student1.first_name == "John"
        assert student1.last_name == "Doe"
        assert student1.age == 20
        assert student1.admission_number == 1234
        assert student1.is_qualified == True

    def test_str_method(self, student1):
        assert student1.__str__() == "John"

    def test_grade_method_A(self, student1):
        assert student1.get_grade() == "A"

    def test_grade_method_B(self, student1):
        student1.average_score = 70
        assert student1.get_grade() == "B"

    def test_grade_method_C(self, student1):
        student1.average_score = 50
        assert student1.get_grade() == "C"

    def test_grade_method_D(self, student1):
        student1.average_score = 30
        assert student1.get_grade() == "D"

    def test_grade_returns_none(self, student1):
        student1.average_score = None
        assert student1.get_grade() is None

    def test_username_is_created(self, student1):
        assert student1.username == "john-doe"


class TestStudentsAPIView:
    def test_list_students_empty_array_if_not_students(self, client, url_students_list):
        response = client.get(url_students_list)
        assert response.status_code == 200
        assert response.data == []

    def test_list_students(self, client, url_students_list, student1):
        response = client.get(url_students_list)
        assert response.status_code == 200
        assert response.data[0]["first_name"] == "John"

    def test_create_student(self, client, url_students_list):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "age": 20,
            "admission_number": 1234,
            "is_qualified": True,
            "average_score": 90,
        }
        response = client.post(url_students_list, data=data)
        assert response.status_code == 201
        assert response.data["first_name"] == "Jane"
        assert response.data["last_name"] == "Doe"
        assert response.data["age"] == 20
        assert response.data["admission_number"] == 1234
        assert response.data["is_qualified"] == True
        assert response.data["average_score"] == 90

    def test_retrieve_student(
        self, client, url_retrieve_update_destroy_student, student1
    ):
        response = client.get(url_retrieve_update_destroy_student)
        assert response.status_code == 200
        assert response.data["first_name"] == "John"
        assert response.data["last_name"] == "Doe"
        assert response.data["age"] == 20
        assert response.data["admission_number"] == 1234
        assert response.data["is_qualified"] == True
        assert response.data["average_score"] == 90

    def test_update_student(
        self, client, url_retrieve_update_destroy_student, student1
    ):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 26,
            "admission_number": 1234,
            "is_qualified": True,
            "average_score": 90,
        }
        response = client.put(
            url_retrieve_update_destroy_student,
            data=data,
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.data["first_name"] == "John"
        assert response.data["last_name"] == "Doe"
        assert response.data["age"] == 26
        assert response.data["admission_number"] == 1234
        assert response.data["is_qualified"] == True
        assert response.data["average_score"] == 90

    def test_delete_student(
        self, client, url_retrieve_update_destroy_student, student1
    ):
        response = client.delete(url_retrieve_update_destroy_student)
        assert response.status_code == 204


class TestClassroomModel:
    def test_classroom_can_be_created(self, classroom1):
        assert classroom1.name == "Class 1"
        assert classroom1.student_capacity == 10

    def test_str_method(self, classroom1):
        assert classroom1.__str__() == "Class 1"


class TestClassroomList:
    def test_list_classrooms(
        self,
        client,
        classroom1,
        url_list_classrooms,
    ):
        response = client.get(url_list_classrooms)
        assert response.status_code == 200
        assert response.data[0]["name"] == "Class 1"

    def test_empty_list_classrooms(self, client, url_list_classrooms):
        response = client.get(url_list_classrooms)
        assert response.status_code == 200
        assert response.data == []

    def test_create_classroom(self, client, url_list_classrooms, user_token):
        data = {"name": "Class 1", "student_capacity": 10}
        headers = {"Authorization": f"Token {user_token}"}
        response = client.post(
            url_list_classrooms,
            data=data,
            headers=headers,
        )
        assert response.status_code == 201
        assert response.data["name"] == "Class 1"
        assert response.data["student_capacity"] == 10

    def test_create_classroom_with_no_name(
        self, client, url_list_classrooms, user_token
    ):
        data = {"student_capacity": 20}
        headers = {"Authorization": f"Token {user_token}"}
        response = client.post(url_list_classrooms, data=data, headers=headers)
        assert response.status_code == 400
        assert response.data["name"] == ["This field is required."]

    def test_retrieve_classroom(self, client, url_retrieve_update_destroy_classroom):
        response = client.get(url_retrieve_update_destroy_classroom)
        assert response.status_code == 200
        assert response.data["name"] == "Class 1"
        assert response.data["student_capacity"] == 10

    def test_update_classroom(self, client, url_retrieve_update_destroy_classroom):
        data = {"name": "Class 2", "student_capacity": 20}
        response = client.put(
            url_retrieve_update_destroy_classroom,
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.data["name"] == "Class 2"
        assert response.data["student_capacity"] == 20

    def test_delete_classroom(self, client, url_retrieve_update_destroy_classroom):
        response = client.delete(url_retrieve_update_destroy_classroom)
        assert response.status_code == 204
