import ast
import logging
import datetime
import traceback
import threading

from django.views.generic.base import TemplateView

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from core import models, serializers, constants, utils
from core.commit_input_handler import main


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
        pd = utils.PastDayReport()
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
        """ Pushes data to MQ client, which handles processing and saving to database
        """
        # Todo : Do data send task as well in background(may be through threading)
        mq_client = main.ProcessData()
        try:
            download_thread = threading.Thread(target=process_data.run_consumer)
            download_thread.start()
            mq_client.push_data({
                'project': request.data.get('project'),
                'lint_report': request.data.get('lint_report'),
                'total_changes': request.data.get('total_changes'),
                'email': request.data.get('email'),
                'username': request.data.get('username'),
            })
        except:
            logger.error('Error pushing data to MQ: %s' % traceback.print_exc())

        return Response({constants.SUCCESS: True}, status=status.HTTP_201_CREATED)


class CodeBoard(TemplateView):
    """Overall dashboard"""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(CodeBoard, self).get_context_data(**kwargs)
        reports = utils.DashboardReports()
        context.update(reports.reports())
        return context


class UserIssues(TemplateView):
    """Controller for handling user issues page"""

    template_name = 'user_issues.html'

    def get_context_data(self, **kwargs):
        context = super(UserIssues, self).get_context_data(**kwargs)
        context.update(utils.IssueReports.weekly_user_issue_report(kwargs.get('user_id')))
        return context


class UserCompare(TemplateView):
    """Create view for compare users"""

    template_name = 'compare.html'

    def get_context_data(self, **kwargs):
        context = super(UserCompare, self).get_context_data(**kwargs)
        if self.request.GET.get('u_1') and self.request.GET.get('u_2') \
            and self.request.GET.get('w'):
            context.update(utils.CompareUser.compare(self.request.GET.get('u_1'), 
                self.request.GET.get('u_2'), self.request.GET.get('w')))
        else:
            context.update({'error': 'user ids missing or date range missing'})
        return context