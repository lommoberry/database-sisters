from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    # path("results/", views.results, name="results")
    path("results/", views.results, name="results")
]
# Bridget Kim xpt3bn