import re
import traceback

from django.db import models
from django.contrib.auth.models import User

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

    def create_commit_entry(self, lint_report, change_details, email, username):
        """Creates commit data entry"""
        from core.models import CommitData
        self.email = email
        self.username = username
        user = self.get_user()
        if not user:
            return constants.USER_DOES_NOT_EXIST
        cd = CommitData(lint_report=lint_report, user=user, change_details=change_details)
        cd.save()
        return constants.SUCCESS


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
