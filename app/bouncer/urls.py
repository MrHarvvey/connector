from django.urls import path

from bouncer import views

urlpatterns = [
    path('', views.landing, name='landing')
]