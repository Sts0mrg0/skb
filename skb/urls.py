"""skb URL Configuration

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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap

from core.sitemaps import *

sitemaps = {
    'index': IndexSitemap,
    'posts': PostSitemap,
    'flatpages': FlatPageSitemap,
    'standartmodels': StandardModelSitemap,
    'works': WorksSitemap,
    'workid': WorksIDSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('pl/', include('photolog.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('contact/', include('contact.urls')),
    path('', include('core.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
