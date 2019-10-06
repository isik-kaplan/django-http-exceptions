"""REST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('from_status/<int:status>/', views.from_status),
    path('from_name/<str:name>/', views.from_name),
    path('with_response/', views.with_response),
    path('with_content/', views.with_content),
    path('exception/', views.exception),
    path('errorify/403/', views.errorify_403),
    path('errorify/404/', views.Errorify404.as_view()),
    path('not_found/', views.not_found)
]
