"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mysite import settings
from django.contrib.auth import views as auth_views
from blog.forms import AuthenticationFormWithChekUsersStatus

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    url(r'^login/$', auth_views.LoginView.as_view(authentication_form = AuthenticationFormWithChekUsersStatus)),
    url(r'^logout/$', auth_views.LogoutView,{'next_page':'/index/'}, name='logout')

]


