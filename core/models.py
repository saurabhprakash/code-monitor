from django.db import models
from django.contrib import admin

from jsonfield import JSONField

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CodeStandardData(BaseModel):
    """code standards data"""

    project = models.CharField(max_length=255, db_index=True)
    score = models.DecimalField(max_digits=19, decimal_places=10)
    metadata = JSONField(null=True, blank=True)
    report = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)


admin.site.register(CodeStandardData)