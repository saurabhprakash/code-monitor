import datetime

from django.views.generic.base import TemplateView

from rest_framework.decorators import detail_route
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import CodeStandardData
from core.serializers import CodeStandardDataSerializer
from core.utils import PastDayReport


class MonitorView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
            mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = CodeStandardData.objects.all()
    serializer_class = CodeStandardDataSerializer

    def create(self, request, format=None):
        print ('request.data=', request.POST)
        serializer = CodeStandardDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     print (serializer.validated_data)
    #     serializer.save()


class ReportView(TemplateView):
    """Generate reports
    """

    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        pd = PastDayReport()
        context['results'] = pd.generate()
        return context
