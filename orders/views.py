from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import View

from customers.models import Customer
from robots.models import Robot
from orders.models import Order
from orders.forms import OrderForm
from rabbit import get_rabbit_channel


ROBOT_NOT_FOUND_MESSAGE = (
    "В данный момент робота нет в наличии. "
    "Как только робот будет произведён, "
    "на Вашу почту будет отправлено письмо."
)


class OrderSingleView(View):
    http_method_names = ["post"]

    def post(self, request):
        """
        POST: {"customer_email": "string", "robot_serial": "string"}
        :param request:
        :return:
        """
        # В случае наличия нужного робота создаётся заказ
        # В ином случае заказ добавляется в очередь сообщений, на которые
        # отправляется письмо при создании нужного робота.
        order = OrderForm(request.POST)

        if order.is_valid():
            order_data = order.cleaned_data
            existed_robot = Robot.objects.filter(
                serial=order_data["robot_serial"],
                ordered=False,
            ).all()[:1]
            if len(existed_robot) == 0:
                # Добавление заказа в очередь RabbitMQ, т.к. робот не найден
                with get_rabbit_channel() as channel:
                    channel.queue_declare(queue=order_data["robot_serial"])
                    channel.basic_publish(
                        exchange="",
                        routing_key=order_data["robot_serial"],
                        body=order_data["customer_email"],
                    )
                return JsonResponse(
                    {
                        "status": "ok",
                        "detail": ROBOT_NOT_FOUND_MESSAGE,
                    },
                    status=200,
                    json_dumps_params={"ensure_ascii": False},
                )

            customer = Customer.objects.get_or_create(
                email=request.POST.get("customer_email")
            )[0]
            created_order = Order.objects.create(
                customer=customer, robot_serial=existed_robot[0].serial
            )
            existed_robot[0].ordered = True
            existed_robot[0].save()
            return JsonResponse(model_to_dict(created_order), status=200)

        return JsonResponse(order.errors, status=400)
