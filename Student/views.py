# views.py
from rest_framework.decorators import action ,api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status , viewsets
from django.shortcuts import get_object_or_404
from authentification.models import Course, Enrollment , Material , Assignment , Submission , Grade , ReadingState, InteractionHistory
from .permissions import IsStudent
from authentification.serializers import SubmissionSerializer,GradeSerializer,EnrollmentSerializer , MaterialSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.none()
     
    def perform_create(self,serializer):
        serializer.save(student=self.request.user)
    def create(self, request, *args, **kwargs):
     print(request.data)
     
     course_id = request.data.get('course')
     if not course_id:
        return Response(
            {'status': 'error', 'message': 'Course ID is required for enrollment.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

     course = get_object_or_404(Course, id=course_id)
     enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)

     if created:
       # print(f"Enrolled user {request.user.username} in course {course.title}")
        return Response(
            {'status': 'success', 'message': f'Enrolled in {course.title}.'},
            status=status.HTTP_201_CREATED,
        )
     else:
        #print(f'User {request.user.username} is already enrolled in course {course.title}')
        return Response(
            {'status': 'error', 'message': f'Already enrolled in {course.title}.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
   
    
class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = MaterialSerializer
    queryset = Material.objects.none()
    #queryset = Material.objects.all()
    
    @action(detail=True, methods=['post'])
    def save_reading_progress(self, request, material_id):
        material = self.get_object()
        reading_state, created = ReadingState.objects.get_or_create(
            student=request.user, material=material
        )
        reading_state.reading_state = request.data.get('reading_state', reading_state.reading_state)
        reading_state.save()
        return Response({'status': 'success', 'message': 'Reading progress saved successfully.'})

    @action(detail=True, methods=['post'])
    def track_interaction(self, request, material_id):
        material = self.get_object()
        course = material.course
        InteractionHistory.objects.create(student=request.user, course=course, material=material)
        return Response({'status': 'success', 'message': 'Interaction tracked successfully.'})





class SubmissionViewSet (viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.none()

    def create(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        submission_content = request.data.get('submission_content')
        Submission.objects.create(student=request.user, assignment=assignment, submission_content=submission_content)
        return Response(
            {'status': 'success', 'message': f'Submitted assignment for {assignment.title}.'},
            status=status.HTTP_201_CREATED,
        )



class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = GradeSerializer
    queryset = Grade.objects.none()
    def get_queryset(self):
        grades = Grade.objects.filter(student=self.request.user)
        grade_data = [{'assignment_title': grade.assignment.title, 'grade': grade.grade, 'feedback': grade.feedback} for grade in grades]
        return Response(grade_data)



    





