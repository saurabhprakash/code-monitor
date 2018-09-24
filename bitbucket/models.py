import logging

from django.db import models
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex

from core import models as core_models
from bitbucket import manager


logger = logging.getLogger(__name__)
decorators = [csrf_exempt, ]


class BitbucketActivity(core_models.BaseModel):
    """
    Bit bucket Dump from web-hooks

    For PR metadata needs to have following field:
        pr id,
        for approval or comments, PR author information
        reviewers
        comment list
    """
    MAJOR_TYPE = (
        ('push', 'Push'),
        ('pullrequest', 'PR'),
    )
    SUB_TYPE = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('approved', 'Approved'),
        ('approval_removed', 'Approval removed'),
        ('merged', 'Merged'),
        ('declined', 'Declined'),
        ('comments_created', 'Comments created'),
        ('comments_updated', 'Comments updated'),
        ('comments_deleted', 'Comments deleted'),
    )
    STATE = (
        ('O', 'Open'),
        ('M', 'Merged'),
        ('D', 'Declined')
    )

    type_of_activity = models.CharField(max_length=20, choices=MAJOR_TYPE)
    sub_type = models.CharField(max_length=20, choices=MAJOR_TYPE, blank=True, null=True)

    actor_username = models.CharField(max_length=50)
    actor_display_name = models.CharField(max_length=50)

    project_full_name = models.CharField(max_length=100)
    state = models.CharField(max_length=1, choices=STATE, blank=True, null=True)

    # pr or push id
    content_id = models.CharField(max_length=30, db_index=True, blank=True, null=True)

    metadata = JSONField()

    objects = manager.BitbucketActivityManager()

    class Meta:
        indexes = [
            GinIndex(fields=['metadata']),
            models.Index(fields=['created_at']),
            models.Index(fields=['created_at', 'actor_username']),
            models.Index(fields=['created_at', 'project_full_name']),
            models.Index(fields=['created_at', 'type_of_activity', 'sub_type', 'actor_username']),
        ]

    def __str__(self):
        return "actor: %s, project:%s" % (self.name, self.project_full_name)


admin.site.register(BitbucketActivity)
