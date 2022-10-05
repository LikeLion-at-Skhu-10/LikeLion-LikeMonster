from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage_edit/', views.mypage_edit, name='mypage_edit'),
    path('password_edit/', views.password_edit, name='password_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)