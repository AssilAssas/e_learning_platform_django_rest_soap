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


router = DefaultRouter()

#router.register(r'users', CustomUserViewSet, basename='user')



router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')



router.register(r'assignments', AssignmentViewSet, basename='assignment')

router.register(r'submissions', SubmissionViewSet, basename='submission')



router.register(r'interactionhistories', InteractionHistoryViewSet, basename='interactionhistory')

router.register(r'readingstates', ReadingStateViewSet, basename='readingstate')

urlpatterns = [
    path('manage', include(router.urls)),
    
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('register/', UserRegister.as_view(), name='user-register'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    


]
