from datetime import datetime

from django.db import models

from bitbucket import constants as bitbucket_constants


class CodeRepoDataBaseManager(models.Manager):
    """
    CodeRepoDataBase Manager
    """

    def get_push_queryset(self, start: datetime, end: datetime):
        """
        Get the push for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for push data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset().\
            filter(type_of_activity=bitbucket_constants.PUSH,
                   created_at__range=(start, end))

    def get_pull_queryset(self, start: datetime, end: datetime):
        """
        Get the pull for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for pull data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=bitbucket_constants.PULL_REQUEST,
                   created_at__range=(start, end)).distinct('content_id')

    def get_merged_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get merged pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for merged pull data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=bitbucket_constants.PULL_REQUEST, state='M',
                   created_at__range=(start, end)).distinct('content_id')

    def get_open_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get open pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for open pull request data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=bitbucket_constants.PULL_REQUEST, state='O',
                   created_at__range=(start, end)).distinct('content_id')

    def get_comments_on_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get comments on pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for comment related to pull request data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=bitbucket_constants.PULL_REQUEST,
                   sub_type=bitbucket_constants.COMMENT,
                   created_at__range=(start, end))

    def get_approvals_on_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get approvals on pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for approvals related to pull request data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=bitbucket_constants.PULL_REQUEST,
                   sub_type=bitbucket_constants.APPROVAL,
                   created_at__range=(start, end))
