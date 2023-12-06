"""
URL configuration for e_learning_platform_django_rest_soap_graphQL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
<<<<<<< HEAD
    # path('admin/', admin.site.urls),
    path("authentification/",include("authentification.urls")),
    path("student/",include("Student.urls")),
    path("adminstrator/",include("adminstrator.urls")),
=======
    path('admin/', admin.site.urls),
    path("",include("authentification.urls")),
    path("",include("Student.urls")),
   # path("",include("Tutor.urls")),
>>>>>>> 80f63e9d4f1dd26f5ecbd3a670a105b621c87dd6
]   
