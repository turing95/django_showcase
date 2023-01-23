from django.core.management.base import BaseCommand

from api.models import Employee, Department, SubDepartment
from api.serializers import EmployeeCreateSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json


class Command(BaseCommand):

    def handle(self, verbosity=1, *args, **kwargs):
        if Employee.objects.exists() is False:
            user = User.objects.create_superuser(username='clipboard',password='clipboard')
            Token.objects.create(user=user)
            f = open('demo_data/data.json')
            data = json.load(f)
            for x in data:
                employee_serializer = EmployeeCreateSerializer(data=x)
                employee_serializer.is_valid()
                employee_serializer.save()
            self.stdout.write(self.style.SUCCESS("Data initialized"))
        else:
            self.stdout.write(self.style.SUCCESS("Data already initialized"))
