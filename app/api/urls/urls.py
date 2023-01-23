from django.urls import path
from api import views
urlpatterns = [
    path('ss/', views.overall_ss,name="overall_ss"),
    path('departments/ss/', views.departments_ss,name='departments_ss'),
    path('sub_departments/ss/', views.sub_departments_ss,name='sub_departments_ss')
]
