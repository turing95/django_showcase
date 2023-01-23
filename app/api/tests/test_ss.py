from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Employee, Department, SubDepartment
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from api.views import overall_ss,departments_ss,sub_departments_ss
from api.tests.data.expected_results import departments_ss as expected_departments_ss, overall_ss as expected_overall_ss, sub_departments_ss as expected_sub_departments_ss


class OverallSSTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='marco')
        self.department = Department.objects.create(name='dep')
        self.sub_department = SubDepartment.objects.create(name='subdep', department=self.department)
        self.employee = Employee.objects.create(name='marco', department=self.department,
                                                sub_department=self.sub_department, currency=Employee.Currency.EUR,
                                                salary=150000, on_contract=True)
        self.employee_1 = Employee.objects.create(name='marco', department=self.department,
                                                  sub_department=self.sub_department, currency=Employee.Currency.INR,
                                                  salary=100000, on_contract=False)

    def overall_ss(self, data=None, auth=True):
        factory = APIRequestFactory()
        url = reverse('overall_ss')
        request = factory.get(
            url,
            data,
            content_type='application/json',
        )
        if auth is True:
            force_authenticate(
                request,
                user=self.user,
            )
        return overall_ss(request)

    def test_overall_ss(self):
        response = self.overall_ss()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(
            set(response.data.keys()),
            expected_overall_ss,
            set(response.data.keys()),
        )

    def test_overall_ss_no_auth(self):
        """
        Ensure we can create a new employee object.
        """

        response = self.overall_ss(auth=False)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_overall_ss_params(self):
        response = self.overall_ss(data={'on_contract': True, 'currency': Employee.Currency.EUR})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(
            set(response.data.keys()),
            expected_overall_ss,
            set(response.data.keys()),
        )
        self.assertEqual(response.data['average_salary'],
                         Employee.objects.get(on_contract=True, currency=Employee.Currency.EUR).salary)

    def test_overall_ss_wrong_params(self):
        response = self.overall_ss(data={'on_contract': 'fsdas', 'currency': 'ffa'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)


class DepartmentsSSTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='marco')
        self.department = Department.objects.create(name='dep')
        self.department_1 = Department.objects.create(name='dep_1')
        self.sub_department = SubDepartment.objects.create(name='subdep', department=self.department)
        self.sub_department_1 = SubDepartment.objects.create(name='subdep_!', department=self.department_1)
        self.employee = Employee.objects.create(name='marco', department=self.department,
                                                sub_department=self.sub_department, currency=Employee.Currency.EUR,
                                                salary=150000, on_contract=True)
        self.employee_1 = Employee.objects.create(name='marco', department=self.department_1,
                                                  sub_department=self.sub_department_1, currency=Employee.Currency.INR,
                                                  salary=100000, on_contract=False)

    def departments_ss(self, auth=True):
        factory = APIRequestFactory()
        url = reverse('departments_ss')
        request = factory.get(
            url,
            content_type='application/json',
        )
        if auth is True:
            force_authenticate(
                request,
                user=self.user,
            )
        return departments_ss(request)

    def test_departments_ss(self):
        response = self.departments_ss()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        for x in response.data:
            self.assertEqual(
                set(x.keys()),
                expected_departments_ss,
                set(x.keys()),
            )

    def test_departments_ss_no_auth(self):
        """
        Ensure we can create a new employee object.
        """

        response = self.departments_ss(auth=False)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)


class SubDepartmentsSSTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='marco')
        self.department = Department.objects.create(name='dep')
        self.department_1 = Department.objects.create(name='dep_1')
        self.sub_department = SubDepartment.objects.create(name='subdep', department=self.department)
        self.sub_department_1 = SubDepartment.objects.create(name='subdep_1', department=self.department)
        self.sub_department_2 = SubDepartment.objects.create(name='subdep_2', department=self.department_1)
        self.employee = Employee.objects.create(name='marco', department=self.department,
                                                sub_department=self.sub_department, currency=Employee.Currency.EUR,
                                                salary=150000, on_contract=True)
        self.employee_1 = Employee.objects.create(name='marco', department=self.department_1,
                                                  sub_department=self.sub_department_1, currency=Employee.Currency.INR,
                                                  salary=100000, on_contract=False)

    def sub_departments_ss(self, auth=True):
        factory = APIRequestFactory()
        url = reverse('sub_departments_ss')
        request = factory.get(
            url,
            content_type='application/json',
        )
        if auth is True:
            force_authenticate(
                request,
                user=self.user,
            )
        return sub_departments_ss(request)

    def test_sub_departments_ss(self):
        response = self.sub_departments_ss()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        for x in response.data:
            self.assertEqual(
                set(x.keys()),
                expected_sub_departments_ss,
                set(x.keys()),
            )

    def test_sub_departments_ss_no_auth(self):
        """
        Ensure we can create a new employee object.
        """

        response = self.sub_departments_ss(auth=False)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

