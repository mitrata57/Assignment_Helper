from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import os

"""

#Class validator use garyo vane jaa ja validation chainchha dynamic banauna milchha haamro ma file esma maatra jaane vayera kept it simple
#class banayo vane we make file validators.py ani class bhitra constructor ra __call__ functions to initialize and call the functions
Gemini said
In Python, the __call__ method is a "magic method" that allows an object to behave like a function.

When you add def __call__(self, value): to your FileValidator class, 
you are telling Python: "Whenever someone treats an instance of this class like a function, run this code."
"""
#Yo validate use nagari form ko maatra garyo vane inspect garera accept change garera jun file ni haalna milchha
# def validate_assignment_file(value): 
#     ext = os.path.splitext(value.name)[1].lower()
#     if ext not in ['.pdf', '.docx', '.pptx', '.txt']:
#         raise ValidationError("Only PDF, DOCX, PPTX, and TXT files are allowed.")
    
#     if value.size > 10 * 1024 * 1024: # 10MB
#         raise ValidationError("File is too large (Max 10MB).")

import zipfile
from django.core.exceptions import ValidationError

def validate_assignment_file(file):
    ext = file.name.split('.')[-1].lower()
    file.seek(0)
    if ext not in ['pdf', 'docx', 'pptx', 'txt']:
        raise ValidationError("Only PDF, DOCX, PPTX, and TXT files are allowed.")
    
    if file.size > 10 * 1024 * 1024: # 10MB
        raise ValidationError("File is too large (Max 10MB).")
    
    if ext == "pdf":
        if file.read(4) != b'%PDF':
            raise ValidationError("Invalid PDF file")

    elif ext in ["docx", "pptx"]:
        if file.read(4) != b'PK\x03\x04':
            raise ValidationError("Invalid Office file")
        
        file.seek(0)
        try:
            z = zipfile.ZipFile(file)
            if ext == "docx" and "word/document.xml" not in z.namelist():
                raise ValidationError("Invalid DOCX structure")
            if ext == "pptx" and "ppt/presentation.xml" not in z.namelist():
                raise ValidationError("Invalid PPTX structure")
        except:
            raise ValidationError("Corrupted Office file")

    elif ext == "txt":
        try:
            file.read().decode("utf-8")
        except:
            raise ValidationError("Invalid text file")

    else:
        raise ValidationError("Unsupported file type")    
    

class Assignment(models.Model):
    # Link to the user who created it
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    subject = models.CharField(max_length=200)
    message = models.TextField(verbose_name="Instructions for Experts")
    number_of_pages = models.PositiveIntegerField(default=1)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    respond_message = models.TextField(null = True , blank= True)
    reviewed_at = models.DateTimeField(null=True , blank= True)
    proposal = models.FileField(upload_to= 'uploads/', validators= [validate_assignment_file])
    price = models.FloatField(default= 100)
    response_file = models.FileField(
        upload_to= 'teacher_responses',
        blank= True,
        null= True,
        validators= [validate_assignment_file]
    )

    def __str__(self):
        return f"{self.subject} - {self.user.username}"
    
    def clean(self):
        if hasattr(self, 'user') and self.user and not self.pk:
            pending_count = Assignment.objects.filter(
                user=self.user, 
                status='pending'
            ).count()
            
            if pending_count >= 5:
                raise ValidationError(f"You have {pending_count} pending assignments. Finish them first!")
    def save(self, *args, **kwargs):
            if not self.pk:
               self.full_clean()
            super().save(*args, **kwargs)    
   