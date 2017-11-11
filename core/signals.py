import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from channels import Group

from core import models

@receiver(post_save, sender=models.CommitData)
def create_processed_commit(sender, instance, created, **kwargs):
    """Objective of this signals are following:
        1. Create entry in ProcessedCommitData models corresponding to commit data entry
        2. Calls django channels group send message for last added entry
    """
    if created:
        models.ProcessedCommitData.objects.process_commit_entry(instance)

        Group('socket_report').send({
            'text': json.dumps(models.CommitData.objects.commits_update())
        })
