from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.get_users, name="get_users"),
    path(
        "users/<int:user_id>/calendar/free/",
        views.get_user_calendar_free,
        name="get_user_calendar_free",
    ),
]
