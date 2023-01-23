from .base import BaseModel
from django.db import models


class Department(BaseModel):
    name = models.CharField(max_length=255, unique=True)


class SubDepartment(BaseModel):
    name = models.CharField(max_length=255)
    department = models.ForeignKey('api.Department', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'department'],
                                    name='unique subdepartment for department')
        ]
