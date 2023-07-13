from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from database_sisters.addJournal import views
from database_sisters.search_engine import views

urlpatterns = [
    path("", views.home, name='home'),
    # path("results/", views.results, name="results")
    path("results/", views.results, name="results"),
    path('adding/',views.adding, name="adding"),
    path('admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# Bridget Kim xpt3bn
