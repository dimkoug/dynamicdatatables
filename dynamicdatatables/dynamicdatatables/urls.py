"""
URL configuration for dynamicdatatables project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import IndexView

from .utils import get_data,get_apps,get_models,get_model_fields, get_all_models, get_apps
from .viewsets import DynamicModelViewSet


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('models/', get_models, name='models'),
    path('apps/', get_apps, name='apps'),
    path('data/', get_data, name='data'),
    path('fields/', get_model_fields, name='fields'),
    path('dtables/', DynamicModelViewSet.as_view({'get':'retrieve'}), name='dtables'),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
