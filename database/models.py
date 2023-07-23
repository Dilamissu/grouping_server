from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Image(models.Model):
    data = models.ImageField(upload_to='images/')
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    # [note: 'email/Oauth id/Line id']
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    real_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    slogan = models.CharField(max_length=20)
    introduction = models.TextField()
    photo_id = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL)


class Workspace(models.Model):
    theme_color = models.IntegerField()
    workspace_name = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    is_personal = models.BooleanField()
    photo_id = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(
        User, related_name='joined_workspaces')


class UserTag(models.Model):
    belong_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=20)


class WorkspaceTag(models.Model):
    belong_workspace_id = models.ForeignKey(
        Workspace, on_delete=models.CASCADE)
    content = models.CharField(max_length=20)


class MissionState(models.Model):
    class Stage(models.TextChoices):
        IN_PROGRESS = 'IP', _('in progress')
        PENDING = 'P', _('pending')
        CLOSE = 'C', _('close')
    stage = models.CharField(
        max_length=2, choices=Stage.choices, default=Stage.IN_PROGRESS)
    name = models.CharField(max_length=20)
    belong_workspace_id = models.ForeignKey(
        Workspace, on_delete=models.CASCADE)


class Activity(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    belong_workspace_id = models.ForeignKey(
        Workspace, on_delete=models.CASCADE)
    child_ids = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='parent_ids')
    contributor_ids = models.ManyToManyField(
        User, related_name='contributing_activity_ids')


class Event(models.Model):
    belong_activity_id = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name='event_id', primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    e = models


class Mission(models.Model):
    belong_activity_id = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name='mission_id', primary_key=True)
    deadline = models.DateTimeField()
    state_id = models.ForeignKey(
        MissionState, null=True, blank=True, on_delete=models.SET_NULL)


class Notification(models.Model):
    belong_activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE)
    notify_time = models.DateTimeField()
