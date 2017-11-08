from django.db.models.signals import post_save
from django.dispatch import receiver

from core import models

@receiver(post_save, sender=models.CommitData)
def create_processed_commit(sender, instance, created, **kwargs):
    if created:
        models.ProcessedCommitData.objects.process_commit_entry(instance)
