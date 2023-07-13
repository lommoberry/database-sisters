from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.add_journal_request, name='add'),
    path("add_data/", views.add_data, name='add_data')
]
# Bridget Kim xpt3bn
