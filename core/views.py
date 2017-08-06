from rest_framework.decorators import detail_route
from rest_framework import viewsets, mixins

from core.models import CodeStandardData
from core.serializers import CodeStandardDataSerializer


class MonitorView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
            mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = CodeStandardData.objects.all()
    serializer_class = CodeStandardDataSerializer

    def perform_create(self, serializer):
        serializer.save()
