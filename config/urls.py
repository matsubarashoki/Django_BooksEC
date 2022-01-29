from django.contrib import admin
from django.urls import path

from base import views
urlpatterns = [
    path('admin/', admin.site.urls),

    #index
    path('', views.IndexView.as_view())
]
