from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers

from library_api import api
from library_api import views

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
    url(r'api^', include(router.urls)),
    url(r'^api/member-info/', api.member_info),
    url(r'^api/reserve_book/(?P<book_pk>[0-9]+)/$', api.reserve_book),
    url(r'^api/request_new_book/', api.request_new_book),
    url(r'^api/api-token-auth/', api.member_login, name="member_login"),
]

urlpatterns += (
    # urls for authentication
    url(r'^login/$', auth_views.login, {'template_name': 'authentication/login.html'},
        name='django.contrib.auth.views.login'),
    url(r'changepassword/$', auth_views.password_change, {'template_name': 'authentication/changepassword.html'},
        name='changepassword'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'home/$', views.index, name='home'),
    url(r'home/member-details', views.member_details, name='member_details')
)



