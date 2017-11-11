import ast
import logging

from django.views.generic.base import TemplateView

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from core import models, serializers, constants
from core.utils import PastDayReport


logger = logging.getLogger(__name__)


class MonitorView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
            mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.CodeStandardData.objects.all()
    serializer_class = serializers.CodeStandardDataSerializer

    def create(self, request, format=None):
        serializer = serializers.CodeStandardDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportView(TemplateView):
    """Generate reports
    """

    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        pd = PastDayReport()
        context['results'] = pd.generate()
        return context


class CommitView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
            mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.CommitData.objects.all()
    serializer_class = serializers.CommitDataSerializer

    def create(self, request, format=None):
        response = models.CommitData.objects.create_commit_entry(ast.literal_eval(request.data.get('lint_report')),
                request.data.get('total_changes'), request.data.get('email'), request.data.get('username'))
        if response == constants.SUCCESS:
            return Response({constants.SUCCESS: True}, status=status.HTTP_201_CREATED)
        logger.error('Error: %s' % response)
        return Response({constants.SUCCESS: False, constants.MESSAGE: response}, status=status.HTTP_400_BAD_REQUEST)


class CodeBoard(TemplateView):
    """Overall dashboard"""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(CodeBoard, self).get_context_data(**kwargs)

        return context
