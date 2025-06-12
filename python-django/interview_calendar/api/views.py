from django.http import JsonResponse

from .schedule import calendar_free


def get_users(request):
    return JsonResponse(
        [
            {"id": 1, "name": "User One"},
        ],
        safe=False
    )


def get_user_calendar_free(request, user_id):
    return JsonResponse(calendar_free(user_id), safe=False)
