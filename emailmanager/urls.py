from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from emailmanager.apps import EmailmanagerConfig
from emailmanager.views import home

app_name = EmailmanagerConfig.name

urlpatterns = [

    path('', home, name='parse_emails'),

   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
