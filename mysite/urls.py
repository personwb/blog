"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
import re

from . import settings


def static(prefix, view=serve, **kwargs):
    """
    Helper function to return a URL pattern for serving files in debug mode.

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # ... the rest of your URLconf goes here ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    """
    # No-op if not in debug mode or an non-local prefix
    return url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs)


urlpatterns = [
    url(r'^blog/admin/', admin.site.urls),
    url(r'^blog/blog/', include('blog.urls', namespace='blog')),
    static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
