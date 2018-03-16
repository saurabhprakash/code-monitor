import re
import traceback
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from core import constants


class CommitDataManager(models.Manager):

    def get_user(self):
        """gets users from the given parameters, if email is present uses that else gets from username"""
        try:
            user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=self.username)
            except User.DoesNotExist:
                user = None
        return user

    def create_commit_entry(self, lint_report, change_details, email, username, project):
        """Creates commit data entry"""
        from core.models import CommitData
        self.email = email
        self.username = username if username else email
        user = self.get_user()
        if not user:
            user = User.objects.create_user(self.username, self.email, constants.DEFAULT_PASSWORD)
            user.save()
        cd = CommitData(lint_report=lint_report, user=user, change_details=change_details, project=project)
        cd.save()
        return constants.SUCCESS

    def commits_update(self):
        """:returns response related to all commits"""
        from core.models import CommitData
        last_commit = CommitData.objects.select_related('user').last()
        user_commits_count = CommitData.objects.values('user__email').annotate(number_of_entries=Count('user')).\
            order_by('-number_of_entries')
        return {
            "count": CommitData.objects.count(),
            "last_entry_email": last_commit.user.email,
            "user_commits_count": {user_entry['user__email']: user_entry['number_of_entries'] \
                                   for user_entry in user_commits_count}
        }

    def ranged_query(self, start_date, end_date):
        """Takes start date and end date as parameters
            :returns: CommitData objects for the given date range
        """
        from core.models import CommitData
        return CommitData.objects.select_related('user').filter(created_at__range=(start_date, end_date))

    def get_commits_with_issues_for_user(self, user_id, start_date, end_date):
        """Takes user_id as input and returns commit information for all the commit which 
            has issues with it(for a given date range)
        """
        from core.models import CommitData, ProcessedCommitData
        return CommitData.objects.only('lint_report', 'project').filter(user__id=user_id, 
            created_at__range=(start_date, end_date))
    
    def commit_counts_for_user_in_given_weeks(self, user_id, number_of_weeks):
        """Takes number of weeks and user id as argument and return number of commits for a user
            number_of_weeks should be int
        """
        from core.models import CommitData
        end_date = datetime.datetime.today()
        start_date = end_date + datetime.timedelta(days=-(number_of_weeks*7))
        return CommitData.objects.filter(user__id=user_id, 
            created_at__range=(start_date, end_date)).count()


class ProcessedCommitDataReportManager(models.Manager):

    def create_processed_entries(self, issues, commit_instance):
        """creates entries which can be directly saved in CommitData"""
        from core.models import ProcessedCommitData
        ProcessedCommitData.objects.bulk_create([
            ProcessedCommitData(language=k, issues_count=v, commit_ref=commit_instance) for k, v in issues.items()])

    def process_commit_entry(self, commit_instance):
        """Take CommitData instance as input and processes it saves in format needed(in ProcessedCommitData model)"""
        issue_dict = {}
        for k, v in commit_instance.lint_report.items():
            file_information = k.split(constants.DOT)
            language_file_extension = file_information[constants.FILE_EXTENSIONS_LOCATION_INDEX]
            try:
                if constants.LANGUAGE_FILE_EXTENSIONS[language_file_extension] in issue_dict:
                    issue_dict[constants.LANGUAGE_FILE_EXTENSIONS[language_file_extension]] += len(v.get('comments'))
                else:
                    issue_dict[constants.LANGUAGE_FILE_EXTENSIONS[language_file_extension]] = len(v.get('comments'))
            except Exception as e:
                traceback.print_exc()
        self.create_processed_entries(issue_dict, commit_instance)

    def process_and_save(self, commit_instance):
        """
        Take CommitData instance as input and processes it saves in format needed(in ProcessedCommitData model)

        # Deprecated: Not in use now
        """
        file_found = False
        issue_dict = {}
        found_language = ''
        for line in commit_instance.lint_report.splitlines():
            if not file_found:
                for language, regex in constants.LANGUAGE_FILE_EXTENSIONS_REGEX.items():
                    regexp = re.compile(regex)
                    if regexp.search(line) and not file_found:
                        file_found = True
                        found_language = language
            else:
                if len(line) == 0:
                    file_found = False
                else:
                    issue_dict[found_language] = issue_dict.get(found_language, 0) + 1
        self.create_processed_entries(issue_dict, commit_instance)

    def ranged_query(self, start_date, end_date):
        """Takes start date and end date as parameters
            :returns: ProcessedCommitData objects for the given date range
        """
        from core.models import ProcessedCommitData
        return ProcessedCommitData.objects.select_related('commit_ref__user').\
            filter(commit_ref__created_at__range=(start_date, end_date))
