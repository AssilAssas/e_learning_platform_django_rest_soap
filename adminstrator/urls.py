
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserListView,create_admin_user,user_delete,user_edit,custom_login,dashboard,custom_logout


urlpatterns = [
 #admin
    path('listedit/<int:user_id>/', user_edit, name='user_edit'),
    path('create_admin_user/', create_admin_user, name='create_admin_user'),
    path('delete/<int:user_id>/', user_delete, name='user_delete'),
    #access account
    path('loginadmin/', custom_login, name='loginadmin'),
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('logoutadmin/', custom_logout, name='logout'),
    path('dashboardadmin/', dashboard, name='dashboardadmin'),
]