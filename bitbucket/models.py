import logging

from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from code_repo_base import models as base_models
from bitbucket import manager


logger = logging.getLogger(__name__)
decorators = [csrf_exempt, ]


class BitbucketActivity(base_models.CodeRepoDataBase):
    """
    Bit bucket Dump from web-hooks

    For PR metadata needs to have following field:
        pr id,
        for approval or comments, PR author information
        reviewers
        comment list
    """

    objects = manager.BitbucketActivityManager()

    def __str__(self):
        return "actor: %s, project:%s" % (self.actor_username, self.project_full_name)


admin.site.register(BitbucketActivity)
