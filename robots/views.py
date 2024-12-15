import datetime

from django.http import JsonResponse, FileResponse
from django.db.models import Count
from django.forms.models import model_to_dict
from django.utils import timezone
from django.views.generic import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from robots.forms import RobotForm
from robots.models import Robot
from utils import create_excel_file


@method_decorator(csrf_exempt, name="dispatch")
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


EXCEL_COLUMNS_NAMES = ("Модель", "Версия", "Количество за неделю")


class RobotsGetExcel(View):
    http_method_names = ["get"]

    def get(self, request):
        week_ago = timezone.now() - datetime.timedelta(weeks=1)

        robots_models = (
            Robot.objects.values("model").filter(created__gte=week_ago).distinct()
        )
        robots_data = {}
        for row in robots_models:
            model = row["model"]
            robots = (
                Robot.objects.values("model", "version")
                .filter(model__exact=model, created__gte=week_ago)
                .annotate(s_count=Count("version"))
            )
            robots_list = [list(robot.values()) for robot in robots]
            if len(robots_list) > 0:
                robots_data[model] = robots_list

        virtual_file = create_excel_file(EXCEL_COLUMNS_NAMES, robots_data)

        return FileResponse(virtual_file, filename="robots.xlsx")
