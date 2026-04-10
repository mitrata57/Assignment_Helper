from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'deadline', 'status', 'created_at','respond_message','reviewed_at')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('subject', 'message', 'user__username')
    
    # This makes the date hierarchy clickable at the top
    date_hierarchy = 'deadline'