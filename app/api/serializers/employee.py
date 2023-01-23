from rest_framework import serializers
from api.models import Employee, Department, SubDepartment


class EmployeeCreateSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    department = serializers.CharField()
    sub_department = serializers.CharField()

    class Meta:
        model = Employee
        fields = (
            'uuid', 'created_at', 'updated_at', 'name', 'salary', 'currency', 'department', 'sub_department',
            'on_contract')


    def create(self, validated_data):
        dep = validated_data.pop('department')
        sub_dep = validated_data.pop('sub_department')
        department_instance, created = Department.objects.get_or_create(name=dep)
        sub_department_instance, created = SubDepartment.objects.get_or_create(name=sub_dep,department=department_instance)
        employee_instance = Employee.objects.create(**validated_data, department=department_instance,sub_department=sub_department_instance)
        return employee_instance
