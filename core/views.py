import ast
import logging

from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from core import models, serializers, constants, utils


logger = logging.getLogger(__name__)
decorators = [csrf_exempt, ]

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
        project = models.CommitData.clean_project_name(request.data.get('project') \
            if request.data.get('project') else '')
        response = models.CommitData.objects.create_commit_entry(\
            ast.literal_eval(request.data.get('lint_report')), 
            request.data.get('total_changes'), request.data.get('email').rstrip(), 
            request.data.get('username').rstrip(), project)
        if response == constants.SUCCESS:
            return Response({constants.SUCCESS: True}, status=status.HTTP_201_CREATED)
        logger.error('Error: %s' % response)
        return Response({constants.SUCCESS: False, constants.MESSAGE: response}, 
            status=status.HTTP_400_BAD_REQUEST)


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


class MailReport(TemplateView):
    """Mail reports
    """

    template_name = 'mail.html'

    def get_context_data(self, **kwargs):
        context = super(MailReport, self).get_context_data(**kwargs)
        reports = utils.MailReport()
        context.update(reports.prepare_report())
        return context


class LeadReports(TemplateView):
    """LeadReports
    """
    template_name = 'no_commit.html'

    def get_context_data(self, **kwargs):
        context = super(LeadReports, self).get_context_data(**kwargs)
        reports = utils.LeadReports()
        weeks = int(context['view'].request.GET.get('weeks')) \
            if context['view'].request.GET.get('weeks') else 1
        context.update(reports.get_lead_report(weeks))
        return context

    
class UserReport(TemplateView):
    """UserReport
    """
    template_name = 'user-report.html'

    def get_context_data(self, **kwargs):
        context = super(UserReport, self).get_context_data(**kwargs)
        context.update({'users': User.objects.only('first_name', 'last_name').\
            filter(is_active=True, is_staff=False)})
        return context
