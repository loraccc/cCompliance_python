from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("appCategory.urls")),
    path('appSec/', include("appSection.urls")),
]
