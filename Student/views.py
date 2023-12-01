# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from authentification.models import Course, Enrollment , Material , Assignment , Submission , Grade , ReadingState, InteractionHistory
from .permissions import IsStudent


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the user is already enrolled in the course
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        # Enroll the student in the course
        Enrollment.objects.create(student=request.user, course=course)
        return Response({'status': 'success', 'message': f'Enrolled in {course.title}.'})
    else:
        return Response({'status': 'error', 'message': f'Already enrolled in {course.title}.'})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStudent])
def view_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    # You may want to add logic to check if the student is enrolled in the course
    
    material_data = {
        'title': material.title,
        'description': material.description,
        'upload_date': material.upload_date,
        'document_type': material.document_type,
        # Add any additional fields as needed
    }

    return Response(material_data)










@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        # Handle form submission and save the submission
        submission_content = request.data.get('submission_content')
        Submission.objects.create(student=request.user, assignment=assignment, submission_content=submission_content)
        return Response({'status': 'success', 'message': f'Submitted assignment for {assignment.title}.'})
    
    return Response({'status': 'error', 'message': 'Invalid request method.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStudent])
def view_grades(request):
    grades = Grade.objects.filter(student=request.user)
    grade_data = [{'assignment_title': grade.assignment.title, 'grade': grade.grade, 'feedback': grade.feedback} for grade in grades]
    return Response(grade_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])
def save_reading_progress(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    # Update or create the reading state
    reading_state, created = ReadingState.objects.get_or_create(student=request.user, material=material)
    
    # Update the reading state based on the request data
    reading_state.reading_state = request.data.get('reading_state', reading_state.reading_state)
    reading_state.save()

    return Response({'status': 'success', 'message': 'Reading progress saved successfully.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])
def track_interaction(request, course_id, material_id):
    course = get_object_or_404(Course, id=course_id)
    material = get_object_or_404(Material, id=material_id)
    
    # Log the interaction in the history
    InteractionHistory.objects.create(student=request.user, course=course, material=material)
    
    return Response({'status': 'success', 'message': 'Interaction tracked successfully.'})



