from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = "user"
        ordering = ['date_joined']
        
        
    def __str__(self):
        return self.username
class Course(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=150)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_capacity = models.IntegerField()
    
    class Meta:
        db_table = "course"
        ordering = ['title']
        
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
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
    class Meta:
        db_table = "material"
        ordering = ["upload_date"]
        
class Assignment(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    class Meta:
        db_table = "assignment"
        ordering = ["due_date"]
class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_content = models.CharField(max_length=150)
    submission_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "submission"
        ordering = ["submission_date"]  
    
class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.IntegerField()
    feedback = models.TextField(max_length=150)
    class Meta:
        db_table = "grade"
        ordering = ["grade"]
class InteractionHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    interaction_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "interaction_history"
        ordering = ["interaction_date"]
class ReadingState(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    reading_state = models.IntegerField()
    last_read_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "reading_state"
        ordering = ["reading_state"]
    
