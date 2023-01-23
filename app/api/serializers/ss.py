from rest_framework import serializers
from api.models import Employee, Department, SubDepartment


class OverallSSRequestSerializer(serializers.Serializer):
    on_contract = serializers.BooleanField(required=False)
    currency = serializers.ChoiceField(Employee.Currency.choices, required=False)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class OverallSSResponseSerializer(serializers.Serializer):
    average_salary = serializers.FloatField()
    max_salary = serializers.IntegerField()
    min_salary = serializers.IntegerField()

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class DepartmentSSResponseSerializer(serializers.ModelSerializer):
    average_salary = serializers.FloatField()
    max_salary = serializers.IntegerField()
    min_salary = serializers.IntegerField()

    class Meta:
        model = Department
        fields = (
            'name', 'average_salary', 'max_salary', 'min_salary')


class SubDepartmentSSResponseSerializer(serializers.ModelSerializer):
    average_salary = serializers.FloatField()
    max_salary = serializers.IntegerField()
    min_salary = serializers.IntegerField()
    department_name = serializers.CharField(source='department.name')

    class Meta:
        model = SubDepartment
        fields = (
            'name', 'department_name', 'average_salary', 'max_salary', 'min_salary')
