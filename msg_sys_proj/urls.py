from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="abra Home Assignment - Messaging System")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view),
    path('msg/', include('msg_sys_app.urls')),
    path('accounts/', include('accounts.urls')),
]
