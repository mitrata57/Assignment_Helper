# assignments/views.py
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from .forms import AssignmentOrderForm 
from . models import Assignment
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
"""
@login_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentOrderForm(request.POST , request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user 
            assignment.save()
            return redirect('home') 
    else:
        form = AssignmentOrderForm()
    
    return render(request, 'assignments/order_form.html', {'form': form})

"""
from django_ratelimit.decorators import ratelimit
@ratelimit(key='ip', rate='3/m', block=True)
@login_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentOrderForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            
            try:
                assignment.full_clean() 
                assignment.save()
                messages.success(request, "Assignment submitted!")
                return redirect('home')
            except ValidationError as e:
                form.add_error(None, e) #catches the limit reached error from the model
    else:
        form = AssignmentOrderForm()
    
    return render(request, 'assignments/order_form.html', {'form': form})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment,pk=pk)
    if request.user.is_superuser or request.user.role== "teacher":
         return render (request, 'assignments/assignment_detail.html',{'assignment' : assignment})
    if assignment.user == request.user:
         return render (request, 'assignments/assignment_detail.html',{'assignment' : assignment})


@ratelimit(key='ip', rate='5/m', block=True)
@login_required
def respond_to_assignment(request, pk):
    # IDENTITY CHECK
    if not (request.user.is_superuser or request.user.role == "teacher"):
        return HttpResponse("You do not have permission to respond.", status=401)

    assignment = get_object_or_404(Assignment, pk=pk)

    if request.method == 'POST':
        teacher_text = request.POST.get('expert_answer')
        teacher_file = request.FILES.get('solution_file')

        if teacher_text:
            assignment.respond_message = teacher_text
            # Only update file if a new one is provided
            if teacher_file:
                assignment.response_file = teacher_file

            assignment.status = 'completed'
            assignment.reviewed_at = timezone.now()
            
            assignment.save()
            messages.success(request, "Solution submitted successfully!")
            return redirect('assignment_detail', pk=assignment.pk)

    return render(request, 'assignments/respond_form.html', {'assignment': assignment})