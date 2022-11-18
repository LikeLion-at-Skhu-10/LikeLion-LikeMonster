from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('window/', views.window, name='window'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
