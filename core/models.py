import ast

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import ArrayField

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

    lint_report = JSONField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change_details = JSONField(null=True, blank=True)
    project = models.CharField(max_length=255, db_index=True, default="")

    objects = manager.CommitDataManager()

    def __str__(self):
        return "id: %s, user: %s, time: %s" % (self.pk, self.user.username, self.created_at)

    @staticmethod
    def clean_project_name(project_name):
        """if project name contains a url process and get project name from it"""
        if '/' in project_name:
            return project_name.split('/')[-1]
        return project_name

    @staticmethod
    def add_data(project, lint_report, total_changes, email, username):
        project = CommitData.clean_project_name(project if project else '')
        CommitData.objects.create_commit_entry(ast.literal_eval(lint_report),
                total_changes, email, username, project)


class ProcessedCommitData(models.Model):
    """Processed data for commit"""
    language = models.CharField(max_length=100)
    issues_count = models.PositiveIntegerField()
    commit_ref = models.ForeignKey(CommitData)
    meta_data = JSONField(default={})

    objects = manager.ProcessedCommitDataReportManager()

    def __str__(self):
        return "id:%s, commit-id: %s, language: %s" % (self.pk, self.commit_ref.id, self.language)


class ProjectTagging(models.Model):
    """Project Name and Tag association"""
    tag = models.CharField(max_length=100, db_index=True)
    projects = ArrayField(models.CharField(max_length=200), blank=True)

    class Meta:
        indexes = [GinIndex(fields=['projects'])]

    def __str__(self):
        return "tag: %s" % self.tag


class ProjectUsers(models.Model):
    """Model for project and associated users
        users field are list of users who are present in project
        project_names are list of project names, which may be present on bitbucket/repo,
            for e.g Project "name" may be "abc" and "project_names" will be "abc_backend",
                "abc_frontend" etc
    """
    name = models.CharField('Project Name', max_length=100, db_index=True)
    users = ArrayField(models.PositiveIntegerField(), blank=True)
    project_names = ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self):
        return "name: %s" % self.name


admin.site.register(CodeStandardData)
admin.site.register(CommitData)
admin.site.register(ProcessedCommitData)
admin.site.register(ProjectTagging)
admin.site.register(ProjectUsers)
