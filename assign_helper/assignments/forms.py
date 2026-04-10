from django import forms
from .models import Assignment

class AssignmentOrderForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'message', 'number_of_pages', 'deadline','price','proposal']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}), # This makes the deadline a clickable calendar picker in the browser
            'message': forms.Textarea(attrs={'rows': 4}),
            'proposal': forms.FileInput(attrs={
                'accept': '.pdf,.docx,.pptx', # Tells the browser to filter files
                    'required': 'true' })
                                    
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border-2 border-slate-300 rounded-lg focus:border-blue-500 focus:outline-none'
            })
        

