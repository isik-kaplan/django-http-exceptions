"""REST URL Configuration"""

from django.urls import path

from . import views

urlpatterns = [
    path("from_status/<int:status>/", views.from_status),
    path("from_name/<str:name>/", views.from_name),
    path("with_response/", views.with_response),
    path("with_content/", views.with_content),
    path("with_json/", views.with_json),
    path("exception/", views.exception),
    path("errorify/403/", views.errorify_403),
    path("errorify/404/", views.Errorify404.as_view()),
    path("not_found/", views.not_found),
]
