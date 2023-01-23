from rest_framework import viewsets, mixins

from api.models import Employee
from api.serializers import EmployeeCreateSerializer
from rest_framework.permissions import IsAuthenticated


class EmployeeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
        - Extends only create and destroy mixin to expose only Create and Delete
        - get_serializer_class is a useful method that can return a serializer based on the needed action to be perfomed
    """
    lookup_field = 'uuid'
    serializer_action_classes = {
        'create': EmployeeCreateSerializer
    }
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(EmployeeViewSet, self).get_serializer_class()
