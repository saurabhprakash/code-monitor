from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from jsonfield import JSONField

from core import manager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CodeStandardData(BaseModel):
    """code standards data"""

    project = models.CharField(max_length=255, db_index=True)
    score = models.DecimalField(max_digits=25, decimal_places=20)
    metadata = JSONField(null=True, blank=True)
    report = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.project, self.score, self.created_at)


class CommitData(BaseModel):
    """commit data model, contains data for each commit save in field data(which is a text)"""

    data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = manager.CommitDataManager()

        
admin.site.register(CodeStandardData)
admin.site.register(CommitData)
