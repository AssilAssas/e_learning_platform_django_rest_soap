from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, MaterialViewSet, SubmissionViewSet, GradeViewSet

""" urlpatterns = [
    
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('material/<int:material_id>/', view_material, name='view_material'),
    path('submit_assignment/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
    path('save_reading_progress/<int:material_id>/', save_reading_progress, name='save_reading_progress'),
    path('track_interaction/<int:course_id>/<int:material_id>/', track_interaction, name='track_interaction'),
    path('view_grades/', view_grades, name='view_grades'),   
    
    
    # Other URL patterns
] """



router = DefaultRouter()
# i wanna include the course_id in url patterns in enroll

router.register(r'enroll', EnrollmentViewSet, basename='enrollment')
router.register(r'material', MaterialViewSet, basename='material')
router.register(r'submit_assignment', SubmissionViewSet, basename='submission')
router.register(r'view_grades', GradeViewSet, basename='grade')


urlpatterns = [
    path('', include(router.urls)),
    path('enroll/<int:course_id>/', include(router.urls)),
]
