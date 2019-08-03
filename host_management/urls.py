from django.conf.urls import include, url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'host', views.HostViewSet, base_name=views.Host)

urlpatterns = [
    url('', include(router.urls)),
]
