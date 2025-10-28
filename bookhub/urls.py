"""
URL configuration for bookhub project.

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
# bookhub/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # library app first
    path('api/library/', include('library.urls')),

    # accounts / auth after library
    path('api/accounts/', include('accounts.urls')),

    # admin and other global routes
    path('admin/', admin.site.urls),
]
