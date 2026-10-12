from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

def index(request):
    notices = Notice.objects.all().order_by('-id')
    return render(request,'index.html',locals())

def notice_detail(request,notice_id):
    notice = get_object_or_404(Notice,id=notice_id)
    return render(request,'notice_detail.html',locals())

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = "Please enter your correct password and username."
    return render(request,'admin_login.html',locals())

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_classes = Class.objects.count()
    total_results = Result.objects.values('student').distinct().count()
    return render(request,'admin_dashboard.html',locals())

def admin_logout(request):
    logout(request)
    return redirect('admin-login')

@login_required  
def create_class(request):
    if request.method == 'POST':
        try:
            class_name = request.POST.get('classname')
            class_numeric = request.POST.get('classnamenumeric')
            section = request.POST.get('section')
            Class.objects.create(class_name=class_name,class_numeric=class_numeric,section=section)
            messages.success(request,"Class created successfully")
            return redirect('create_class')
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('create_class')
    return render(request,'create_class.html') 

from django.shortcuts import get_object_or_404
@login_required  
def manage_classes(request):
    classes = Class.objects.all()

    if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            class_obj = get_object_or_404(Class,id=class_id)
            class_obj.delete()
            messages.success(request,"Class deleted Successfull")
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_classes')    
    return render(request,'manage_classes.html',locals()) 

@login_required  
def edit_class(request,class_id):
    class_obj = get_object_or_404(Class,id=class_id)
    if request.method == 'POST':
        class_name = request.POST.get('classname')
        class_numeric = request.POST.get('classnamenumeric')
        section = request.POST.get('section')
        try:
            class_obj.class_name = class_name
            class_obj.class_numeric = class_numeric
            class_obj.class_section = section
            class_obj.save()
            messages.success(request,"Class updated successfully")
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_classes')
    return render(request,'edit_class.html',locals()) 

@login_required  
def create_subject(request):
    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subjectname')
            subject_code= request.POST.get('subjectcode')
            Subject.objects.create(subject_name=subject_name,subject_code=subject_code)
            messages.success(request,"Subject created successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('create_subject')
    return render(request,'create_subject.html')


@login_required  
def manage_subject(request):
    subjects = Subject.objects.all()

    if request.GET.get('delete'):
        try:
            subject_id = request.GET.get('delete')
            subject_obj = get_object_or_404(Subject,id=subject_id)
            subject_obj.delete()
            messages.success(request,"Subject deleted Successfull")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_subject') 
           
    return render(request,'manage_subject.html',locals())

@login_required  
def edit_subject(request,subject_id):
    subject_obj = get_object_or_404(Subject,id=subject_id)
    if request.method == 'POST':
        subject_name = request.POST.get('subjectname')
        subject_code = request.POST.get('subjectcode')
        try:
            subject_obj.subject_name = subject_name
            subject_obj.subject_code = subject_code
            subject_obj.save()
            messages.success(request,"subject updated successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_subject')
    return render(request,'edit_subject.html',locals()) 

@login_required  
def add_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            subject_id = request.POST.get('subject')
            SubjectCombination.objects.create(student_class_id=class_id,subject_id=subject_id,status=1)
            messages.success(request,"Subject combination added successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('add_subject_combination')
    return render(request,'add_subject_combination.html',locals())



@login_required  
def manage_subject_combination(request):
    combinations = SubjectCombination.objects.all()
    aid = request.GET.get('aid')
    if request.GET.get('aid'):
        try:
            SubjectCombination.objects.filter(id = aid).update(status=1)
            messages.success(request,"Subject Combination activated Successfull")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_subject_combination') 
           
    did = request.GET.get('did')
    if request.GET.get('did'):
        try:
            SubjectCombination.objects.filter(id = did).update(status=0)
            messages.success(request,"Subject Combination deactivated Successfull")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_subject_combination')
    return render(request,'manage_subject_combination.html',locals())


@login_required  
def add_student(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('fullname')
            roll_id = request.POST.get('rollid')
            email = request.POST.get('emailid')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            class_id = request.POST.get('class')
            student_class =  Class.objects.get(id=class_id)
            Student.objects.create(name=name,roll_id=roll_id,email=email,gender=gender,dob=dob,student_class =student_class)
            messages.success(request,"Student info added successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('add_student')
    return render(request,'add_student.html',locals())


@login_required  
def manage_students(request):
    students = Student.objects.all()

    return render(request,'manage_students.html',locals()) 

@login_required  
def edit_student(request,student_id):
    student_obj = get_object_or_404(Student,id=student_id)
    if request.method == 'POST':
        
        try:
            student_obj.name = request.POST.get('fullname')
            student_obj.rollid = request.POST.get('rollid')
            student_obj.emailid = request.POST.get('emailid')
            student_obj.gender = request.POST.get('gender')
            student_obj.dob= request.POST.get('dob')
            student_obj.status = request.POST.get('status')
            student_obj.save()
            messages.success(request,"Student updated successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_students')
    return render(request,'edit_student.html',locals())


@login_required  
def add_notice(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            details = request.POST.get('details')
            Notice.objects.create(title=title,detail=details)
            messages.success(request,"Notice info added successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('add_notice')
    return render(request,'add_notice.html',locals())


@login_required  
def manage_notice(request):
    notices = Notice.objects.all()

    if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            notice_obj = get_object_or_404(Notice,id=notice_id)
            notice_obj.delete()
            messages.success(request,"Notice deleted Successfull")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('manage_notice') 
           
    return render(request,'manage_notice.html',locals())  


@login_required  
def add_result(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            student_id = request.POST.get('student_id')
            marks_data = {key.split('_')[1]:value for key, value in request.POST.items() if key.startswith('marks_')}
            for subject_id,marks in marks_data.items():
                Result.objects.create(student_id=student_id,student_class_id=class_id,
                                      subject_id=subject_id,marks=marks)
            
            messages.success(request,"Result info added successfully")
            return redirect('add_student')
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('add_result')
    return render(request,'add_result.html',locals())  
    
from django.http import JsonResponse
def get_students_subjects(request):
    class_id = request.GET.get('class_id')

    if class_id:
        students = list(Student.objects.filter(student_class_id=class_id).values('id','name','roll_id'))

        subject_combinations = SubjectCombination.objects.filter(student_class_id=class_id,status=1).select_related('subject')

        subjects = [{'id' : sc.subject.id, 'name':sc.subject.subject_name} for sc in subject_combinations]
        return JsonResponse({'students':students,'subjects':subjects})
    return JsonResponse({'students':[],'subjects':[]})


@login_required  
def manage_result(request):
    results = Result.objects.select_related('student','student_class').all()
    students = {}
    for res in results:
          stu_id = res.student.id
          if stu_id not in students:
            students[stu_id] = {
                'student' : res.student,
                'student_class' : res.student_class,

            }
           
    return render(request,'manage_result.html',{'results' : students.values()})  

@login_required  
def edit_result(request,stid):
    student = get_object_or_404(Student,id=stid)
    results = Result.objects.filter(student=student)
    if request.method == 'POST':
        ids = request.POST.getlist('id[]') # id[]: [5,6,7]
        marks = request.POST.getlist('marks[]') # marks[]: [34,56,78]

        for i in range(len(ids)):
            result_obj = get_object_or_404(Result,id=ids[i])
            result_obj.marks = marks[i]
            result_obj.save()
        messages.success(request,'Result updated Successfully')
        # return redirect('edit_result',stid=student.id)
        return redirect('manage_result')
    return render(request,'edit_result.html',locals()) 

from django.contrib.auth import update_session_auth_hash
@login_required  
def change_password(request):

    if request.method == 'POST':
        old = request.POST['old_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if new != confirm:
            messages.error(request,'New Password and confirm password do not match.')
            
        user = authenticate(username=request.user.username,password=old)

        if user:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Password updated Successfully')
            return redirect('change_password')
        else: 
            messages.success(request,'old password is incorrect')
            return redirect('change_password')    
    return render(request,'change_password.html')  


def search_result(request):
    classes = Class.objects.all()    
    return render(request,'search_result.html',locals())  

def check_result(request):
    if request.method == 'POST':
        rollid = request.POST['rollid']
        class_id = request.POST['class']
        print(rollid)

        print(class_id)
        try:
            student = Student.objects.get(roll_id=rollid,student_class_id=class_id)
            results = Result.objects.filter(student=student)

            total_marks = sum([r.marks for r in results])
            subject_count = results.count()
            max_total = subject_count * 100

            percentage = (total_marks/max_total) * 100 if max_total > 0 else 0 
            percentage = round(percentage,2)
            return render(request,'result_page.html',locals()) 
        except Exception as e:
                    messages.error(request,f"No result found for given Roll ID and Class.")
                    return redirect('search_result')    
     