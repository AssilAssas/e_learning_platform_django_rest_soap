from django.urls import path
from . import views

urlpatterns = [
    # update the url files with reference to the views
    
    path('register/',views.UserRegister.as_view()),
    path('login/',views.UserLogin.as_view()),
    path('logout/',views.UserLogout.as_view()),
    path('user/',views.UserView.as_view()),
    
    
]
