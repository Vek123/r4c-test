from django.urls import path

from robots.views import RobotSingleView


urlpatterns = [
    path("robots/", RobotSingleView.as_view()),
]
