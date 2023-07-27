from django.urls import path
from .views import GoogleSocialAuthView, LineSocialAuthView, GitHubSocialAuthView, LogoutView

urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view()),
    path("line/", LineSocialAuthView.as_view()),
    path("github/", GitHubSocialAuthView.as_view()),
    path("logout/", LogoutView.as_view()),
]