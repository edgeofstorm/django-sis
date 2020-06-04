from django import forms
from .models import Exam
# import os

class ExamCreateForm(forms.ModelForm):
    sheet = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    class Meta:
        model = Exam
        # if you dont want to add timestamp use this
        fields = ('title','klass','sheet')

    # def clean_sheet(self,*args,**kwargs):
    #     sheet = request.POST.get('sheet')
    #     ext = os.path.splitext(sheet)[1]
    #     valid_exts=['.pdf','.xls','.xlsx','.docx','.doc']
    #     if not ext in valid_exts:
    #         raise forms.ValidationError('unsupported file extension')
    #     return sheet