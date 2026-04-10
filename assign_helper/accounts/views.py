from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from assignments.models import Assignment 
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse


@ratelimit(key='ip', rate='5/m', method=['GET', 'POST'], block=True)
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.role = "student"
            user.save()
            login(request, user) 
            return redirect('home') 
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')
    
    if request.user.is_superuser or request.user.role == 'teacher':
        requests = Assignment.objects.all().order_by('-created_at')
        return render(request, 'staff_dashboard.html', {'assignments': requests})

    user_assignments = Assignment.objects.filter(user=request.user).order_by('-created_at')
    pending_assign = Assignment.objects.filter(user = request.user,status = "pending").count()
    completed_assign = Assignment.objects.filter(user = request.user,status = "completed").count()
    return render(request, 'dashboard.html', {'assignments': user_assignments,'pending_assign': pending_assign,'completed_assign':completed_assign})


from django.contrib.auth.views import LoginView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='5/m', method=['POST','GET'], block=True), name='dispatch')
class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
