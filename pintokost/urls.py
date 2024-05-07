"""pintokost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from house import views as house_views

urlpatterns = [
    path('', house_views.index),
    path('admin/', admin.site.urls),
    path('house/', include('house.urls', namespace='house')),
    path('k/<int:pk>/<str:slug>', house_views.KuitansiView.as_view(), name='kuitansi'),
    path('login/', auth_views.LoginView.as_view(template_name='house/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('profile/', include('profile.urls', namespace='profile')),
    path("select2/", include("django_select2.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
