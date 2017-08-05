from rest_framework.decorators import detail_route
from rest_framework import viewsets

from core.models import CodeStandardData
from core.serializers import CodeStandardDataSerializer


class MonitorView(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = CodeStandardData.objects.all()
    serializer_class = CodeStandardDataSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
