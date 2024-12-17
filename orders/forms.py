from django import forms


class OrderForm(forms.Form):
    customer_email = forms.EmailField()
    robot_serial = forms.CharField()
