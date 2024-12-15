from django.urls import path

from robots.views import RobotSingleView, RobotsGetExcel


urlpatterns = [
    path("robots/", RobotSingleView.as_view()),
    path("robots/excel", RobotsGetExcel.as_view()),
]
