from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Min, Max
from api.models import Employee, Department, SubDepartment
from api.serializers import OverallSSRequestSerializer, OverallSSResponseSerializer, DepartmentSSResponseSerializer, SubDepartmentSSResponseSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def overall_ss(request):
    """

    """
    serializer = OverallSSRequestSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        queryset = Employee.objects.all()
        on_contract = serializer.validated_data.get('on_contract', None)
        if on_contract is not None:
            queryset = queryset.filter(on_contract=on_contract)

        currency = serializer.validated_data.get('currency', None)
        if currency is not None:
            queryset = queryset.filter(currency=currency)

        ss = queryset.aggregate(average_salary=Avg('salary'), min_salary=Min('salary'),
                                max_salary=Max('salary'))
        serializer = OverallSSResponseSerializer(ss)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def departments_ss(request):
    ss = Department.objects.annotate(average_salary=Avg('employees__salary'), min_salary=Min('employees__salary'),
                                     max_salary=Max('employees__salary'))
    return Response(DepartmentSSResponseSerializer(ss, many=True).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sub_departments_ss(request):
    ss = SubDepartment.objects.annotate(average_salary=Avg('employees__salary'), min_salary=Min('employees__salary'),
                                        max_salary=Max('employees__salary'))
    return Response(SubDepartmentSSResponseSerializer(ss, many=True).data, status=status.HTTP_200_OK)


'''@api_view(["GET"])
def sub_department_ss(request, department_name, sub_department):
    job = DispatchedJob.objects.get(uuid=job_uuid)
    task = DispatchedTask.objects.get(uuid=task_uuid)

    if job not in DispatchedJob.get_compatible_job_with_tasks([task]):
        raise NotCompatibleJobException

    if task.job:
        raise TaskConflictException

    task.job = job
    task.save()
    return Response(status=status.HTTP_201_CREATED)'''
