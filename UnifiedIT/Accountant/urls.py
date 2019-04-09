from django.conf.urls import url
from . import views

app_name = 'Accountant'

urlpatterns = [
    url(r'^get_account/', views.get_account, name="get_account"),
    url(r'^login/', views.admin_login, name='admin_login'),  # Institute Admin Login URL
    url(r'^logout/', views.admin_logout, name='admin_logout'),
]
