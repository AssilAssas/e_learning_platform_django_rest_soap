# can u do the imports ?
from django.urls import path
from .views import initiate_voice_call
from .views import GradeViewSet, CourseViewSet , MaterialViewSet
#import router
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'grades', GradeViewSet, basename='grade')

urlpatterns = [
    path('voice/', initiate_voice_call, name='initiate_voice_call'),
     path('grades/', GradeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('courses/', CourseViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]
