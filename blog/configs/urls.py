from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import ObtainJWTView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', ObtainJWTView.as_view(), name='create_jwt'),
    path('auth/', include('djoser.urls.jwt')),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
