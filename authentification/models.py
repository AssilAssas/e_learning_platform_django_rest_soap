from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser 
from django.utils import timezone  
from django.contrib.auth.models import BaseUserManager


 

class AppUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)

        user_role = extra_fields.pop('role', None)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.date_joined = timezone.now()
        user.set_password(password)

        if user_role:
            user.role = user_role

        user.save(using=self._db)
        return user

    def delete_user(self, email):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.get(email=email)
        user.delete()
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  

        return self.create_user(email, first_name, last_name, password, **extra_fields)






# class AppUserManager(BaseUserManager):
#     def create_user(self,first_name,last_name, email,role, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not password:
#             raise ValueError("Users must have a password")
#         email = self.normalize_email(email)
#         user = self.model(email=email ,first_name=first_name, last_name=last_name, role=role)
        
#         user.role = role
#         user.date_joined = timezone.now()
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#     def delete_user(self,email):
#         if not email:
#             raise ValueError('Users must have an email address')
#         user = self.get(email=email)
#         user.delete()
#         return user
    
#     def create_superuser(self, email, first_name, last_name, role, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, first_name, last_name, role, password, **extra_fields)
    
    # def create_superuser(self,email,password=None):
        
    #     if not email:
    #         raise ValueError('Users must have an email address')
    #     if not password:
    #         raise ValueError("Users must have a password")
    #    # email = self.normalize_email(email)
    #     user = self.create_user(email,password)
    #     user.role = "admin"
    #     user.date_joined = timezone.now()
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    
    # def create_tutor(self,email,password=None):
    #     if not email:
    #         raise ValueError('Users must have an email address')
    #     if not password:
    #         raise ValueError("Users must have a password")
    #     email = self.normalize_email(email)
    #     user = self.model(email=email)
    #     user.role = "tutor"
        
    #     user.date_joined = timezone.now()
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    
    
# CustomUser model    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=150)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    objects = AppUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    
# Course model 
class Course(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=150)
    tutor = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    enrollment_capacity = models.IntegerField()
    class Meta:
        db_table = "course"
        ordering = ['title']
        
class Enrollment(models.Model):
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "enrollment"
        ordering = ["enrollment_date"]


class Material(models.Model):
    title = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    document_type = models.CharField(max_length=150)
    document = models.FileField(upload_to='materials/',default='default.pdf')  
    class Meta:
        db_table = "material"
        ordering = ["upload_date"]
        
class Assignment(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    graded = models.BooleanField(default=False) 
    class Meta:
        db_table = "assignment"
        ordering = ["due_date"]

class Submission(models.Model):
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_content = models.CharField(max_length=150)
    submission_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "submission"
        ordering = ["submission_date"]  
    
class Grade(models.Model):
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.IntegerField()
    feedback = models.TextField(max_length=150)
    class Meta:
        db_table = "grade"
        ordering = ["grade"]




class InteractionHistory(models.Model):
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    interaction_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "interaction_history"
        ordering = ["interaction_date"]

class ReadingState(models.Model):
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    reading_state = models.IntegerField()
    last_read_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "reading_state"
        ordering = ["reading_state"]
 



class PlatformAnalytics(models.Model):

    def __str__(self):
        return f"{self.date} - {self.activity} - {self.user}"