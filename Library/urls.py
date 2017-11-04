from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from library_api import api

router = routers.DefaultRouter()
router.register(r'category', api.CategoryViewSet)
router.register(r'authors', api.AuthorViewSet)
router.register(r'books', api.BookViewSet)
router.register(r'request_book', api.RequestedBookViewSet, 'request_book')
router.register(r'burrowed_book', api.BurrowedBooksViewset, 'burrowed_book')
router.register(r'reserved_book', api.ReservedBookViewSet, 'reserved_book')

urlpatterns = [
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^member-info/', api.member_info),
    url(r'^reserve_book/(?P<book_pk>[0-9]+)/$', api.reserve_book),
    url(r'^request_new_book/', api.request_new_book),
    url(r'^api-token-auth/', api.member_login, name="member_login"),

]
