
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "create-certificate/",
        views.create_certificate,
        name="create_certificate"
    ),
    path(
        "verify/<uuid:certificate_id>/",
        views.verify_certificate,
        name="verify_certificate"
    ),
]
