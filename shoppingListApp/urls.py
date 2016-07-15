from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.signUpLogIn, name='signUp'),
    url(r'^home/(?P<string>[\w\-]+)/$', views.home, name='home'),
    url(r'^headerSignIn/$', views.headerSignIn, name='headerSignIn'),
    url(r'^clearAll/$', views.clearAll, name='clearAll'),
    url(r'^addItemShoppingCart/$', views.addItemShoppingCart, name='addItemShoppingCart'),
]