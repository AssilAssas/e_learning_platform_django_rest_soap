from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class GradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class InteractionHistoryViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    queryset = InteractionHistory.objects.all()
    serializer_class = InteractionHistorySerializer

class ReadingStateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ReadingState.objects.all()
    serializer_class = ReadingStateSerializer

    