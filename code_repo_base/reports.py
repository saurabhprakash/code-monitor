from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict


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
        super(CompanyLevel).__init__(self, start_time, end_time)

    def generate_report(self) -> Dict:
        response = {}

        return response


class ProjectLevel(ReportPointers):

    def __init__(self, start_time: datetime, end_time: datetime):
        super(CompanyLevel).__init__(self, start_time, end_time)
        self.developer_performance_map = {}

    def generate_report(self) -> Dict:
        pass


class IndividualReports(ReportPointers):

    def __init__(self, start_time: datetime, end_time: datetime):
        super(IndividualReports).__init__(self, start_time, end_time)

    def generate_report(self) -> Dict:
        pass


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

    def set_project_level_report(self, start_time, end_time):
        pl = ProjectLevel(start_time, end_time)
        self.report.project_level = pl.generate_report()

    def set_individual_level_report(self, start_time, end_time):
        il = IndividualReports(start_time, end_time)
        self.report.individual_level = il.generate_report()

    def get_report(self):
        return self.report


class ReportGeneration:

    @staticmethod
    def construct_report(start_time, end_time):
        return ReportBuilder()\
            .set_company_level_report(start_time, end_time)\
            .set_project_level_report(start_time, end_time)\
            .set_individual_level_report(start_time, end_time)\
            .get_report()
