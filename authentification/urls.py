from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegister, UserLogin, UserLogout, UserView,
     EnrollmentViewSet,
     AssignmentViewSet,
    SubmissionViewSet, 
    InteractionHistoryViewSet, ReadingStateViewSet,
    CustomUserListCreateView,CustomUserRetrieveUpdateDestroyView,
    
    
)


app_name = 'authentification'
router = DefaultRouter()

#router.register(r'users', CustomUserViewSet, basename='user')



router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')



router.register(r'assignments', AssignmentViewSet, basename='assignment')

router.register(r'submissions', SubmissionViewSet, basename='submission')



router.register(r'interactionhistories', InteractionHistoryViewSet, basename='interactionhistory')

router.register(r'readingstates', ReadingStateViewSet, basename='readingstate')

urlpatterns = [
<<<<<<< HEAD
    path('manage/', include(router.urls)),
    path('grades/', GradeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('courses/', CourseViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
=======
    path('manage', include(router.urls)),
    
>>>>>>> 80f63e9d4f1dd26f5ecbd3a670a105b621c87dd6
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('register/', UserRegister.as_view(), name='user-register'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
<<<<<<< HEAD
    path('voice/', initiate_voice_call, name='initiate_voice_call'),
   
=======
    

>>>>>>> 80f63e9d4f1dd26f5ecbd3a670a105b621c87dd6

]
