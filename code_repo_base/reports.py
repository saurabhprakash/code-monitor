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
        self.number_of_push = CodeRepoDataBase.objects.get_push_queryset\
            (self.start_time, self.end_time).count()
        self.number_of_pr_raised = CodeRepoDataBase.objects.get_pull_queryset\
            (self.start_time, self.end_time).count()
        self.number_of_pr_merged = CodeRepoDataBase.objects.get_merged_pull_request_queryset\
            (self.start_time, self.end_time).count()

        # Comments processing, additional creation of pr_id_set_comments is
        # being done to calculate reviews
        pull_request_comments_qs = CodeRepoDataBase.objects.\
            get_comments_on_pull_request_queryset(self.start_time, self.end_time)
        pr_id_set_comments = set()
        [pr_id_set_comments.add(pr.content_id) for pr in pull_request_comments_qs]
        self.number_of_comments_on_pr = len(pull_request_comments_qs)

        # Approvals processing, additional creation of pr_id_set_approvals is
        # being done to calculate reviews
        pull_request_approvals_qs = CodeRepoDataBase.objects.\
            get_approvals_on_pull_request_queryset(self.start_time, self.end_time)
        pr_id_set_approvals = set()
        [pr_id_set_approvals.add(pr.content_id) for pr in pull_request_approvals_qs]
        self.number_of_approvals_on_pr = len(pull_request_approvals_qs)

        # Reviews processing
        self.number_of_pr_reviewed = len(pr_id_set_comments.union(pr_id_set_approvals))

        # TODO: Check for auto conversion feature
        response = {
            # self.number_of_pr_merged is subtracted from self.number_of_push because for each merge one extra push is created
            'number_of_push': self.number_of_push-self.number_of_pr_merged,
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

    def categorize_based_on_project(self, qs) -> Dict:
        """
        :param qs: queryset which needs to be categorized
        :return: Dict of project -> count map
        """
        report_map = {}
        for entry in qs:
            if entry.project_full_name not in report_map:
                report_map[entry.project_full_name] = 1
            else:
                report_map[entry.project_full_name] += 1
        return report_map

    def generate_report(self) -> Dict:

        self.number_of_push = self.categorize_based_on_project(CodeRepoDataBase.objects\
            .get_push_queryset(self.start_time, self.end_time))

        self.number_of_pr_raised = self.categorize_based_on_project(\
            CodeRepoDataBase.objects.get_pull_queryset\
            (self.start_time, self.end_time))

        self.number_of_pr_merged = self.categorize_based_on_project(\
            CodeRepoDataBase.objects.get_merged_pull_request_queryset\
            (self.start_time, self.end_time))

        # Comments processing, additional creation of pr_id_set_comments is
        # being done to calculate reviews
        pull_request_comments_qs = CodeRepoDataBase.objects.\
            get_comments_on_pull_request_queryset(self.start_time, self.end_time)
        pr_id_set_comments = set()
        content_id_project_map = {}
        for pr in pull_request_comments_qs:
            pr_id_set_comments.add(pr.content_id)
            content_id_project_map[pr.content_id] = pr.project_full_name
        self.number_of_comments_on_pr = self.categorize_based_on_project\
            (pull_request_comments_qs)

        # Approvals processing, additional creation of pr_id_set_approvals is
        # being done to calculate reviews
        pull_request_approvals_qs = CodeRepoDataBase.objects.\
            get_approvals_on_pull_request_queryset(self.start_time, self.end_time)
        pr_id_set_approvals = set()
        for pr in pull_request_approvals_qs:
            pr_id_set_approvals.add(pr.content_id)
            content_id_project_map[pr.content_id] = pr.project_full_name
        self.number_of_approvals_on_pr = self.categorize_based_on_project\
            (pull_request_approvals_qs)

        # Reviews processing
        reviewed_prs = pr_id_set_comments.union(pr_id_set_approvals)
        report_map = {}
        for entry in reviewed_prs:
            if entry not in report_map:
                report_map[content_id_project_map[entry]] = 1
            else:
                report_map[content_id_project_map[entry]] += 1
        self.number_of_pr_reviewed = report_map

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


class IndividualReports(ReportPointers):

    def __init__(self, start_time: datetime, end_time: datetime):
        super(IndividualReports, self).__init__(start_time, end_time)

    def generate_report(self) -> Dict:
        return {
            'commenters_list': [e for e in \
                CodeRepoDataBase.objects.commenters_count\
                (self.start_time, self.end_time)],
            'approvers_list': [e for e in \
                CodeRepoDataBase.objects.reviewers_count\
                (self.start_time, self.end_time)]
        }


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
