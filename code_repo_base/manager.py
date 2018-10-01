from datetime import datetime

from django.db import models

from code_repo_base import constants as code_repo_constants


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
            filter(type_of_activity=code_repo_constants.PUSH,
                   created_at__range=(start, end))

    def get_pull_queryset(self, start: datetime, end: datetime):
        """
        Get the pull for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for pull data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=code_repo_constants.PULL_REQUEST,
                   created_at__range=(start, end)).distinct('content_id')

    def get_merged_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get merged pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for merged pull data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=code_repo_constants.PULL_REQUEST, state='M',
                   created_at__range=(start, end)).distinct('content_id')

    def get_open_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get open pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for open pull request data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=code_repo_constants.PULL_REQUEST, state='O',
                   created_at__range=(start, end)).distinct('content_id')

    def get_comments_on_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get comments on pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for comment related to pull request data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=code_repo_constants.PULL_REQUEST,
                   sub_type=code_repo_constants.COMMENT,
                   created_at__range=(start, end))

    def get_approvals_on_pull_request_queryset(self, start: datetime, end: datetime):
        """
        Get approvals on pull request for all devs for given time range
        :parameter start: start datetime
        :parameter end: end datetime
        :returns: query set for approvals related to pull request data
        """
        return super(CodeRepoDataBaseManager, self).get_queryset(). \
            filter(type_of_activity=code_repo_constants.PULL_REQUEST,
                   sub_type=code_repo_constants.APPROVAL,
                   created_at__range=(start, end))

    def create_entry(self, **kwargs):
        """
        Create an entry to bitbucket activity model,
        :parameter kwargs: has all the fields for entry related to bitbucket activity model
        :returns: Nothing
        """
        super(CodeRepoDataBaseManager, self).get_queryset().create(
            type_of_activity=kwargs.get('type_of_activity'),
            sub_type=kwargs.get('sub_type'),
            actor_username=kwargs.get('author_username'),
            actor_display_name=kwargs.get('author_display_name'),
            project_full_name=kwargs.get('project_full_name'),
            state=kwargs.get('state'),
            content_id=kwargs.get('content_id'),
            metadata=kwargs.get('metadata')
        )


"""

In past month:
    - total number of push: BitbucketActivity.objects.filter(type_of_activity='push', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).count()
    - total number of pull request: BitbucketActivity.objects.filter(type_of_activity='pullrequest', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()
    - BitbucketActivity.objects.filter(type_of_activity='pullrequest', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id')
    - Information of all pr [(pr.content_id, pr.state) for pr in BitbucketActivity.objects.filter(type_of_activity='pullrequest', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id')]
    - merged prs count: BitbucketActivity.objects.filter(type_of_activity='pullrequest', state='M', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()
    - open prs count: BitbucketActivity.objects.filter(type_of_activity='pullrequest', state='O', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()
    - number of comments: BitbucketActivity.objects.filter(type_of_activity='pullrequest', sub_type='comment', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()

"""
