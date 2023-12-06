from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.shortcuts import render
from adminstrator.forms import AdminCreationForm
from authentification.models import CustomUser



# Create your views here.
#adminstrator part
#Admin Actions
#for the dashboard of admin :

def create_admin_user(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password'],
                role='admin'  
            )
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)

            messages.success(request, 'Admin account created successfully!')
            return redirect('dashboard')  
    else:
        form = AdminCreationForm()

    return render(request, 'dashboard.html', {'form': form})



#login of the admin
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('dashboard')
            # else:
            #     return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'dashboard.html')



#logout of the user 
def custom_logout(request):
    pass
    # logout(request)
    # return redirect('/authentification/loginadmin.html/')  




#dashboard of the tutor
# @login_required(login_url='loginadmin')
def dashboard(request):
    students = CustomUser.objects.filter(role='student')
    tutors = CustomUser.objects.filter(role='tutor')
    return render(request, 'dashboard.html', {'students': students, 'tutors': tutors})



#the list of tutors and students by the admin
class UserListView(View):
    template_name = 'user_list.html'
    def get(self, request):
        users = CustomUser.objects.all()
        return render(request, self.template_name, {'users': users})
    
#the adminstrator edit all the users
def user_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = AdminCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = AdminCreationForm(instance=user)
    return render(request, 'user_edit.html', {'form': form, 'user': user})

#the adminstrator delete customUser
def user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

