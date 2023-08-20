from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class Image(models.Model):
    data = models.ImageField(upload_to='images/')
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, account="", user_name = 'unknown', password="", introduction="", slogan=""):
        if account is None:
            raise TypeError('Users must have an id.')

        user = self.model(account=account)
        user.set_password(password)
        user.user_name = user_name
        user.real_name = ''
        user.introduction = introduction
        user.slogan = slogan
        user.photo_id = None
        user.save()

        return user
    
    def create_superuser(self, account, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(account=account, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


    Auth_Providers = {"google": "google", "line": "line", "github": "github"}
    
    """
    Note:objects = UserManager() is required for django to work properly
    It's not the type of this class
    """
class User(AbstractBaseUser, PermissionsMixin):
    # [note: 'email/Oauth id/Line id']
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    real_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    slogan = models.CharField(max_length=20)
    introduction = models.TextField()
    photo_id = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = "account"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return "id:%s user_name:%s" % (self.id, self.user_name)
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)}


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
