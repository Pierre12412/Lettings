from django.contrib import admin
from django.urls import path, include

def trigger_error(request):
    division_by_zero = 1 / 0

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('lettings.urls', namespace='lettings')),
    path('', include('profiles.urls', namespace='profiles')),
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
]
