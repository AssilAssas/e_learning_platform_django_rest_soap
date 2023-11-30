from django.contrib.auth import login, logout
from django.http import HttpResponse
from twilio.twiml.voice_response import VoiceResponse,Gather
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,BasePermission
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserModelSerializer,
    CourseSerializer, EnrollmentSerializer, MaterialSerializer, AssignmentSerializer, SubmissionSerializer, GradeSerializer, InteractionHistorySerializer, ReadingStateSerializer
)
from rest_framework import permissions, status
from .validations import ValidationData
from rest_framework import generics,viewsets
from django.contrib.auth import get_user_model
from .models import CustomUser,Course, Enrollment, Material, Assignment, Submission, Grade, InteractionHistory, ReadingState



UserModel = get_user_model()  


class UserRegister(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # Validate input data
        validation_errors = self.validate_input(request.data)
        if validation_errors:
            return Response({"error": validation_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_obj = serializer.save()

            if user_obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def validate_input(self, data):
        email_error = ValidationData.validate_email(data.get('email', ''))
        password_error = ValidationData.validate_password(data.get('password', ''))

        errors = {}
        if email_error:
            errors['email'] = email_error
        if password_error:
            errors['password'] = password_error

        return errors if errors else None

class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        email = data.get('email', '')

        email_error = ValidationData.validate_email(email)
        password_error = ValidationData.validate_password(data.get('password', ''))

        if email_error:
            return Response({"error": email_error}, status=status.HTTP_400_BAD_REQUEST)

        if password_error:
            return Response({"error": password_error}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            if user is not None:
                login(request, user)
                return Response({"success": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)




class UserLogout(APIView):
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserModelSerializer

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserModelSerializer

#Tutor : 

#Create and manage courses 
class IsTutorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.role == 'tutor')

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated,IsTutorOrAdmin]

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTutorOrAdmin]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.validated_data['tutor'] = self.request.user
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

#Upload course materials, including labs and documents in PDF for material
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    def perform_create(self, serializer):
        serializer.save(
            course=self.get_course(),
            tutor=self.request.user,
        )
    def get_course(self):
        course_id = self.request.data.get('course_id') 
        return Course.objects.get(pk=course_id)  


#Evaluate and provide feedback on student assignments. 
class GradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsTutorOrAdmin]
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def perform_create(self, serializer):
        serializer.save(tutor=self.request.user)

# Initiate voice calls to mark students as absent.
def initiate_voice_call(request):
    response = VoiceResponse()
    response.say("Hello, this is your attendance call. Please press a key to confirm your attendance.")
    response.gather(numDigits=1, action='/confirm_attendance/')
    return HttpResponse(str(response), content_type='text/xml')

def confirm_attendance(request):
    digit_pressed = request.GET.get('Digits')
    return HttpResponse("Confirmation processed.")

def trigger_voice_call(request):
    account_sid = "AC7ee59b1d490616ad7071cb36b1c109a8"
    auth_token = "f4a5989c7566da12eff15f72578e883a"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url=request.build_absolute_uri(reverse('initiate_voice_call')),
        to="+1234567890",
        from_="+14435946087"
    )
    return HttpResponse(f"Voice call SID: {call.sid}")









class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer



class AssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer



class InteractionHistoryViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    queryset = InteractionHistory.objects.all()
    serializer_class = InteractionHistorySerializer

class ReadingStateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ReadingState.objects.all()
    serializer_class = ReadingStateSerializer

    