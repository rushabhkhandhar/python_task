# coinmarketcap_scraper/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/taskmanager/', include('taskmanager.urls')),
]
