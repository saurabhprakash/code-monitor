from django.db import models

from jsonfield import JSONField

from core import models as core_models
from code_repo_base import manager


class CodeRepoDataBase(core_models.BaseModel):
    """
        Base model for code repository,
        It can be extended by concrete implementations like bitbucket or github
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
    sub_type = models.CharField(max_length=20, choices=SUB_TYPE, blank=True, null=True)

    actor_username = models.CharField(max_length=50)
    actor_display_name = models.CharField(max_length=50)

    project_full_name = models.CharField(max_length=100)
    state = models.CharField(max_length=1, choices=STATE, blank=True, null=True)

    # pr or push id
    content_id = models.CharField(max_length=30, db_index=True, blank=True, null=True)

    metadata = JSONField()

    objects = manager.CodeRepoDataBaseManager()

    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'type_of_activity']),
            models.Index(fields=['created_at', 'state', 'type_of_activity']),
            models.Index(fields=['created_at', 'type_of_activity', 'sub_type']),
            models.Index(fields=['created_at', 'type_of_activity', 'sub_type', 'actor_username']),
        ]
        abstract = True
