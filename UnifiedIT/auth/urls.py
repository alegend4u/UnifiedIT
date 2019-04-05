from django.conf.urls import url, include
from . import views

app_name = 'Auth'

urlpatterns = [
    url(r'^get_account/', views.get_account, name="get_account"),
    url(r'^login/', views.user_login, name='user_login'),
]