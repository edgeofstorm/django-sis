from django import template
from django.http import QueryDict

register = template.Library()

@register.filter
def net(value, ders):
    try:
        return 20 - (len(value['Yanlislar'][ders]) + len(value['Yanlislar'][ders])/3 + len(value['Boslar'][ders]))
    except:
        return 0

@register.filter
def get_sol_img(value,args):
    try:
        if args is None:
            return False
        arg_list = [arg.strip() for arg in args.split(',')]
        subject = arg_list[0]
        index = int(arg_list[1])

        # qs = QueryDict(kwargs)
        # print(qs.get('index'),qs.get('subject'))
        #student.exam_results.filter(exam__title='LGS HAZIRLIK - 5').first().exam.solutions.filter(subject='F').first().solutions.solution
        for question in value.solutions.filter(subject=subject).all():
            if index == question.solutions.question:
                return f'{question.solutions.solution.url} {question.solutions}'
        return f"there is no solution for {subject}-{index}"
    except:
        return "hata"
    

@register.filter
def get_str(value):
    try:
        if value is None:
            return ""
        val_list = [val.strip() for val in value.split(',')]
        subject = val_list[0]
        index = int(val_list[1])
        return f'{subject},{index}'
    except:
        return "hata"


@register.simple_tag
def get_img_url(exam, subject, index):
    try:
        #   index = MyModel.objects.filter(sortField__lt = myObject.sortField).count()
        #   list(qs.values_list('id', flat=True)).index(obj.id)
        #   (*qs,).index(instance)
        #   query_Set.extra( raw SQL afterwards)   
        print(exam.solutions.filter(subject=subject).first().solutions.solution.url)
        for exam_solution in exam.solutions.filter(subject=subject).all():
            if int(index) == exam_solution.solutions.question:
                return f'{exam_solution.solutions.solution.url}'
        return ""
        #--{exam_solution.solution}
    except Exception as err:
        #return "{0}".format(err)
        return ""

@register.filter
def label(value):
    if value == 'M':
        return 'Matematik'
    if value == 'S':
        return 'Sosyal'
    if value == 'F':
        return 'Fen'
    if value == 'T':
        return 'Turkce'
    else:
        return 'Brans yok'