"""

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from certificate.views import api as ssl
from domain.views import api as domain
from website.views import api as website
from server.views import api as server
from account.views import api as account
from django.shortcuts import render


urlpatterns = [
    # path('', lambda request: render(request, 'index.html')),
    path('admin/', admin.site.urls),
    path('api/', domain.urls),
    path('api/', website.urls),
    path('api/', ssl.urls),
    path('api/', server.urls),
    path('api/', account.urls),
]