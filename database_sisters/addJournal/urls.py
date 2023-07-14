from django.urls import path


from . import views
# from database_sisters.search_engine import views

urlpatterns = [
    path('adding/',views.adding, name="adding"),
    path('editing/',views.editing, name="editing"),
    path('delete/',views.delete, name="delete"),
    path('success/',views.success, name="success")
]

# Bridget Kim xpt3bn
