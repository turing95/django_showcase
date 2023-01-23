from .base import BaseModel
from django.db import models


class Employee(BaseModel):
    class Currency(models.TextChoices):
        EUR = 'EUR', 'Euro'
        INR = 'INR', 'Indian rupee'
        USD = 'USD', 'US dollar'

    name = models.CharField(max_length=255)
    salary = models.IntegerField()
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
    )
    on_contract = models.BooleanField(default=False)
    department = models.ForeignKey('api.Department', on_delete=models.CASCADE, related_name='employees')
    sub_department = models.ForeignKey('api.SubDepartment', on_delete=models.CASCADE, related_name='employees')
