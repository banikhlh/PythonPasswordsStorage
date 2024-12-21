from django.urls import path

from . import views

urlpatterns = [
    path("", views.password_list, name="password_list"),
    path("add/", views.add_password, name="add_password"),
    path("generate/", views.generate_password_view, name="generate_password"),
]
