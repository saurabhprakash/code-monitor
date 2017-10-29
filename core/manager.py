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

    def create_commit_entry(self, data, email, username):
        """Creates commit data entry"""
        from core.models import CommitData
        self.email = email
        self.username = username
        user = self.get_user()
        if not user:
            return constants.USER_DOES_NOT_EXIST
        cd = CommitData(data=data, user=user)
        cd.save()
        return constants.SUCCESS


class ProcessedCommitDataReportManager(models.Manager):

    def create_processed_entries(self, commit_instance):
        """creates entries which can be directly saved in CommitData"""
        commit_instance
        return []

    def process_and_save(self, commit_instance):
        """Take CommitData instance as input and processes it saves in format needed(in ProcessedCommitData model)"""
        entries = self.create_processed_entries(commit_instance)

        # Bulk create entries
