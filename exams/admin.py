from django.contrib import admin
from .models import Exam, ExamStudentAnswer, ExamResult, ExamSolution, QSolution
# Register your models here.

# class QSolutionInline(admin.TabularInline):
#     model = QSolution

# class ExamSolutionAdmin(admin.ModelAdmin):
#     inlines = [
#         QSolutionInline,
#     ]

admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(ExamStudentAnswer)
admin.site.register(ExamSolution)
admin.site.register(QSolution)
# admin.site.register(ExamSolution, ExamSolutionAdmin)