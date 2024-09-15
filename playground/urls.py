from django.urls import path
from . import views

# URLConf
# every app has a URLConf. views.say_hello doesn't have the parens because we're not calling the function, we're passing a reference to it.
urlpatterns = [path("hello/", views.say_hello)]
