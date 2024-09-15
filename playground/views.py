from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# it's a request handler. It takes a request and returns a response


def calculate():

    x = 1
    y = 2
    return x


def say_hello(request):
    # usually used for:
    # pull data from db
    # mutate data etc
    x = calculate()
    return render(request, "hello.html", {"name": "Worldo"})
