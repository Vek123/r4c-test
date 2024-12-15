from django.forms import ModelForm

from robots.models import Robot


class RobotForm(ModelForm):
    class Meta:
        model = Robot
        fields = "__all__"
