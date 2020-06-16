from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import emp_reg
from .face_capture import gen_emp_face
from .encode_face import gen_emp_data
from .create_result import find_emp
from django.db import IntegrityError
from .models import Employee, Record
from datetime import date, time

IS_LIVE=False
def home(request):
    return render(request, 'homepage.html', {})

def fas_home(request):
    return render(request, 'fas_home.html', {"live":IS_LIVE})

def create_emp(request):
    if request.method == 'POST':
        try: 
            form = emp_reg(request.POST)
            if form.is_valid():
                name=form.cleaned_data['emp_name']
                empid=form.cleaned_data['emp_code']
                employee=Employee()
                employee.emp_name=name
                employee.emp_code=empid
                # val=gen_emp_face(name)
                val=False
                if val:
                    employee.emp_photo=True
                    employee.save()
                
                return render(request, 'cap_res.html', {"complete":val, "name":name})
        except IntegrityError:
            return HttpResponse("User Already exists")
    else:
        form = emp_reg()

    return render(request, 'emp_reg.html', {'form': form})

def cap_res(request):
    if request.method=="POST":
        name=request.POST.get("emp_name")
        employee=Employee.objects.get(emp_name=name)
        encoding=gen_emp_data(name)
        if encoding:
            employee.emp_encoding=True
            employee.save()
            return redirect('fas_home')
        else :
            return HttpResponse("Internal Error")

def start_stop_sys(request):
    global IS_LIVE
    if IS_LIVE:
        name, matches=find_emp()
        if name :
            employee=Employee.objects.get(emp_name=name)
            ent=Record()
            ent.emp_name=employee.emp_name
            ent.emp_code=employee.emp_code
            per=(float(matches)/26) *100
            ent.attendance_confi=per
            ent.attendance_date=date.today()
            ent.attendance_time=time.now()
            if per < 50 :
                ent.remark="Manual Verfication required"
        else :
            return HttpResponse("Intrusion")
    IS_LIVE = not IS_LIVE
    return redirect('fas_home')

def records(request):
    all_records=Record.objects.all().values()
    record_list=list(all_records)
    return JsonResponse(record_list, safe=True)