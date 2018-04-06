from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('spoken.urls')),
    path('spoken/', include('spoken.urls')),
    path('admin/', admin.site.urls),
]
