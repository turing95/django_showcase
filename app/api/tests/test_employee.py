from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Employee, Department, SubDepartment
from api.views import EmployeeViewSet
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
import json
from api.tests.data.expected_results import employee_create


class EmployeeCreateTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='marco')
        self.department = Department.objects.create(name='dep')
        self.department_1 = Department.objects.create(name='dep_1')
        self.sub_department = SubDepartment.objects.create(name='subdep', department=self.department)
        self.sub_department_1 = SubDepartment.objects.create(name='subdep_1', department=self.department_1)

    def create_employee(self, data, auth=True):
        factory = APIRequestFactory()

        request = factory.post(
            reverse('employees-list'),
            data=json.dumps(data),
            content_type='application/json',
        )
        if auth is True:
            force_authenticate(
                request,
                user=self.user,
            )
        view = EmployeeViewSet.as_view({'post': 'create'})
        return view(request)

    def get_mock_creation(self, department_name=None, sub_department_name=None):
        department_name = department_name or self.department.name
        sub_department_name = sub_department_name or self.sub_department.name
        mock = {
            'name': 'marco',
            'currency': Employee.Currency.EUR,
            'salary': 100000,
            'department': department_name,
            'sub_department': sub_department_name
        }
        return mock

    def test_create_employee(self):
        """
        Ensure we can create a new employee object.
        """

        data = self.get_mock_creation()
        response = self.create_employee(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(
            set(response.data.keys()),
            employee_create,
            set(response.data.keys()),
        )
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, data['name'])

    def test_create_employee_new_dept_subdept(self):
        """
        Ensure we can create a new employee object.
        """

        data = self.get_mock_creation(department_name='new_dep',sub_department_name='new_subdep')
        response = self.create_employee(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(
            set(response.data.keys()),
            employee_create,
            set(response.data.keys()),
        )
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, data['name'])

    def test_create_employee_new_subdept_for_dept(self):
        """
        Ensure we can create a new employee object.
        """

        data = self.get_mock_creation(department_name=self.department.name,sub_department_name='new_subdep')
        response = self.create_employee(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(
            set(response.data.keys()),
            employee_create,
            set(response.data.keys()),
        )
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, data['name'])


    def test_create_employee_no_auth(self):
        """
        Ensure we can create a new employee object.
        """

        data = self.get_mock_creation()
        response = self.create_employee(data, auth=False)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)


class EmployeeDestroyTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='marco')
        self.department = Department.objects.create(name='dep')
        self.sub_department = SubDepartment.objects.create(name='subdep', department=self.department)
        self.employee = Employee.objects.create(name='marco', department=self.department,
                                                sub_department=self.sub_department, currency=Employee.Currency.EUR,
                                                salary=150000)

    def destroy_employee(self, pk, auth=True):
        factory = APIRequestFactory()

        request = factory.delete(
            reverse('employees-detail', args=[pk]),
            content_type='application/json',
        )
        if auth is True:
            force_authenticate(
                request,
                user=self.user,
            )
        view = EmployeeViewSet.as_view({'delete': 'destroy'})
        return view(request, uuid=str(pk))

    def test_destroy_employee(self):
        """
        Ensure we can create a new employee object.
        """

        response = self.destroy_employee(pk=self.employee.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(Employee.objects.count(), 0)

    def test_destroy_employee_no_auth(self):
        """
        Ensure we can create a new employee object.
        """

        response = self.destroy_employee(pk=self.employee.pk,auth=False)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)
