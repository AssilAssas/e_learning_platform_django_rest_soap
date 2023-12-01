from django.urls import path
from .views import enroll_course , view_material , submit_assignment , view_grades , save_reading_progress , track_interaction

urlpatterns = [
    
    
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('material/<int:material_id>/', view_material, name='view_material'),
    path('submit_assignment/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
    path('save_reading_progress/<int:material_id>/', save_reading_progress, name='save_reading_progress'),
    path('track_interaction/<int:course_id>/<int:material_id>/', track_interaction, name='track_interaction'),
    path('view_grades/', view_grades, name='view_grades')
    
    
    # Other URL patterns
]
