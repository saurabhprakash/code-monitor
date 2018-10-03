from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict

from code_repo_base.models import CodeRepoDataBase


class ReportPointers(ABC):

    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time

        self.number_of_push = None
        self.number_of_pr_raised = None
        self.number_of_pr_merged = None
        self.number_of_pr_reviewed = None
        self.number_of_comments_on_pr = None
        self.number_of_approvals_on_pr = None

    @abstractmethod
    def generate_report(self) -> Dict:
        pass


class CompanyLevel(ReportPointers):

    def __init__(self, start_time: datetime, end_time: datetime):
        super(CompanyLevel, self).__init__(start_time, end_time)

    def generate_report(self) -> Dict:
        response = {}
        self.number_of_push = CodeRepoDataBase.objects.get_push_queryset\
            (self.start_time, self.end_time).count()
        self.number_of_pr_raised = CodeRepoDataBase.objects.get_pull_queryset\
            (self.start_time, self.end_time).count()
        self.number_of_pr_merged = CodeRepoDataBase.objects.get_merged_pull_request_queryset\
            (self.start_time, self.end_time).count()
        # self.number_of_pr_reviewed =
        self.number_of_comments_on_pr = CodeRepoDataBase.objects.\
            get_comments_on_pull_request_queryset(self.start_time, self.end_time).count()
        self.number_of_approvals_on_pr = CodeRepoDataBase.objects.\
            get_approvals_on_pull_request_queryset(self.start_time, self.end_time).count()

        # TODO: Check for auto conversion feature
        response = {
            'number_of_push': self.number_of_push,
            'number_of_pr_raised': self.number_of_pr_raised,
            'number_of_pr_merged': self.number_of_pr_merged,
            'number_of_pr_reviewed': self.number_of_pr_reviewed,
            'number_of_comments_on_pr': self.number_of_comments_on_pr,
            'number_of_approvals_on_pr': self.number_of_approvals_on_pr
        }
        return response


class ProjectLevel(ReportPointers):

    def __init__(self, start_time: datetime, end_time: datetime):
        super(ProjectLevel, self).__init__(start_time, end_time)
        self.developer_performance_map = {}

    def generate_report(self) -> Dict:
        response = {}
        return response


class IndividualReports(ReportPointers):

    def __init__(self, start_time: datetime, end_time: datetime):
        super(IndividualReports, self).__init__(start_time, end_time)

    def generate_report(self) -> Dict:
        response = {}
        return response


class Report:

    def __init__(self):
        self.company_level = None
        self.project_level = None
        self.individual_level = None


class ReportBuilder:

    def __init__(self):
        self.report = Report()

    def set_company_level_report(self, start_time, end_time):
        cl = CompanyLevel(start_time, end_time)
        self.report.company_level = cl.generate_report()
        return self

    def set_project_level_report(self, start_time, end_time):
        pl = ProjectLevel(start_time, end_time)
        self.report.project_level = pl.generate_report()
        return self

    def set_individual_level_report(self, start_time, end_time):
        il = IndividualReports(start_time, end_time)
        self.report.individual_level = il.generate_report()
        return self

    def get_report(self):
        return self.report


class ReportGeneration:

    @staticmethod
    def construct_report(start_time, end_time):
        report = ReportBuilder()\
            .set_company_level_report(start_time, end_time)\
            .set_project_level_report(start_time, end_time)\
            .set_individual_level_report(start_time, end_time)\
            .get_report()

        return {
            'company': report.company_level,
            'project': report.project_level,
            'individual': report.individual_level
        }
