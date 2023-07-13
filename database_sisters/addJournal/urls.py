from django.urls import path
from django.contrib import admin


from database_sisters.addJournal import views
from database_sisters.search_engine import views

urlpatterns = [
    # path("results/", views.results, name="results")
    path("success/", views.success, name="success"),
    path('adding/',views.adding, name="adding")
]

# Bridget Kim xpt3bn
