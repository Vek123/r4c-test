from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.generic import View

from robots.forms import RobotForm


class RobotSingleView(View):
    http_method_names = ["post"]

    def post(self, request):
        if not request.POST.get("serial"):
            # Генерация поля `serial` в формате `model`-`version` в случае его отсутствия
            prev_mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST["serial"] = (
                f"{request.POST.get("model", "")}-" f"{request.POST.get("version", "")}"
            )
            request.POST._mutable = prev_mutable
        form = RobotForm(request.POST)
        if form.is_valid():
            created_robot = form.save()

            return JsonResponse(model_to_dict(created_robot), status=200)
        else:
            return JsonResponse(form.errors, status=400)
