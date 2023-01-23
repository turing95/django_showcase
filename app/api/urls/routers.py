from rest_framework.routers import SimpleRouter
from api import views

router = SimpleRouter()

router.register(r'employees', views.EmployeeViewSet, basename="employees")
