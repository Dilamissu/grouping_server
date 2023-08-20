from django.db import models
from django.utils.translation import gettext_lazy as _


class Image(models.Model):
    data = models.ImageField(upload_to='images/')
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    # [note: 'email/Oauth id/Line id']
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    real_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    slogan = models.CharField(max_length=20)
    introduction = models.TextField()
    photo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL)


class UserTag(models.Model):
    belong_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tags')
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=20)


class Workspace(models.Model):
    theme_color = models.IntegerField()
    workspace_name = models.CharField(max_length=20)
    description = models.TextField()
    is_personal = models.BooleanField()
    photo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(
        User, related_name='joined_workspaces')


class WorkspaceTag(models.Model):
    belong_workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name='tags')
    content = models.CharField(max_length=20)


class MissionState(models.Model):
    class Stage(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', _('in progress')
        PENDING = 'PENDING', _('pending')
        CLOSE = 'CLOSE', _('close')
    stage = models.CharField(
        max_length=15, choices=Stage.choices, default=Stage.IN_PROGRESS)
    name = models.CharField(max_length=20)
    belong_workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)


class Activity(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    belong_workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE)
    childs = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='parents')
    contributors = models.ManyToManyField(
        User, related_name='contributing_activities')


class ActivityNotification(models.Model):
    belong_activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='notifications')
    notify_time = models.DateTimeField()


class Event(models.Model):
    belong_activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Mission(models.Model):
    belong_activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, primary_key=True)
    deadline = models.DateTimeField()
    state = models.ForeignKey(
        MissionState, null=True, blank=True, on_delete=models.SET_NULL)
