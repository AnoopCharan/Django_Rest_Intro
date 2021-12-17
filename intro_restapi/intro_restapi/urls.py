"""intro_restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls.conf import include
from rest_framework import routers
from api_basic import views
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api_basic.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema', get_schema_view(
                                    title='intro to rest', 
                                    description='first try at REST', 
                                    version='1.0.0' ), 
                                    name='openapi_schema'
                                    ),
    path('docs/', include_docs_urls(title='BlogAPI'))


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]