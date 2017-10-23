from django.conf.urls import url, include
from django.contrib import admin
from library_api import api
from rest_framework import routers
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register(r'category', api.CategoryViewSet)
router.register(r'authors', api.AuthorViewSet)
router.register(r'reservedbook', api.ReservedBookViewSet, 'reservedbook')


urlpatterns = [
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^member-info/', api.member_info),
    url(r'^api-token-auth/', api.member_login, name="member_login"),
]
