from django.urls import path

from robots.views import RobotSingleView, RobotsGetExcel


urlpatterns = [
    path("", RobotSingleView.as_view()),
    path("excel/", RobotsGetExcel.as_view()),
]
