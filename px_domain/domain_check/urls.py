from django.urls import path

from domain_check.api import views

urlpatterns = [
    path(r'check', views.DomainCheckView.as_view()),
]   