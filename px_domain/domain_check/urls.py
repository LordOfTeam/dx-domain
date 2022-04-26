from django.urls import path

from domain_check.api import views

urlpatterns = [
    # path('check', views.DomainCheckView.as_view()),
    path('check/', views.DomainCheckView.as_view()),
]   