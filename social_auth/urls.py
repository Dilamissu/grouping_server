from django.urls import path
from .views import LoginView, GoogleSocialAuthView, LineSocialAuthView, GitHubSocialAuthView, LogoutView

urlpatterns = [
    path("signIn/", LoginView.as_view()),
    path("google/", GoogleSocialAuthView.as_view()),
    path("line/", LineSocialAuthView.as_view()),
    path("github/", GitHubSocialAuthView.as_view()),
    path("logout/", LogoutView.as_view()),
]