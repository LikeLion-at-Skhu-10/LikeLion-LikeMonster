from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('write/', views.write, name='write'),
    path('read/', views.read, name='read'),
    path('detail/<str:id>/', views.detail, name='detail'),
    path('edit/<str:id>/', views.edit, name = 'edit'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('cmt_edit/<str:post_id>/<str:cmt_id>/', views.cmt_edit, name = 'cmt_edit'),
    path('cmt_delete/<str:id>/', views.cmt_delete, name='cmt_delete'),
    path('like/<str:id>/', views.likes, name="likes"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
