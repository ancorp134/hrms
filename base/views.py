
from .models import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime


@login_required(login_url='signin')
def HolidayMaterView(request):
    holidays_records = Holiday.objects.all()

    if request.method == 'POST':
        
        holiday_form = HolidayMasterForm(data=request.POST)
        
        if holiday_form.is_valid():
            holiday_form.save()
            messages.success(request, "Holiday added successfully.")
            return redirect('holiday-master')
    else:
        holiday_form = HolidayMasterForm()

    context = {
        'holidays_records': holidays_records,
        'holiday_form' : holiday_form
    }
    return render(request,'holiday_master.html',context)


@login_required(login_url='signin')
def editHoliday(request,pk):
    holiday = get_object_or_404(Holiday,id=pk)

    if request.method == 'POST':
        holiday_name = request.POST.get('holiday_name')
        state = request.POST.get('state')
        branch = request.POST.get('branch')
        holiday_date = request.POST.get('holiday_date')
        holiday_category = request.POST.get('holiday_category')

        holiday.holiday_name = holiday_name
        holiday.state = state
        branch_id = request.POST.get('branch')
        branch = get_object_or_404(Branch, id=branch_id)
        holiday.branch = branch
        holiday.holiday_date = holiday_date
        holiday.holiday_category = holiday_category
        holiday.save()
        messages.success(request,"Holiday Updated Successfully")
        return redirect("holiday-master")
        
    return render(request,'holiday_master.html')

@login_required(login_url='signin')
def deleteHoliday(request,pk):
    if request.method == 'POST':
        holiday = Holiday.objects.get(id = pk)
        holiday.delete()
        messages.success(request,"Holiday deleted Successfully")
        return redirect("holiday-master")
        
    return render(request,'holiday_master.html')


@login_required(login_url='signin')
def LeaveMasterView(request):
    leave_records = LeaveMaster.objects.all()
    
    if request.method == 'POST':
        
        leave_form = LeaveMasterForm(data=request.POST)
        leave_code = request.POST['leave_code']
        lname = request.POST['leave_name']
        leavecode_exist = LeaveMaster.objects.filter(leave_code=leave_code).exists() or  LeaveMaster.objects.filter(leave_name=lname).exists()

        if leavecode_exist:
        
            messages.error(request, "Leave name or code already Exists")
            return redirect('leave-master')
        
        if leave_form.is_valid():
            leave_form.save()
            messages.success(request, "Leave added successfully.")
            return redirect('leave-master')
    else:
        leave_form = LeaveMasterForm()

    context = {
        'leave_records': leave_records,
        'leave_form': leave_form,
    }
    return render(request, 'leave_master.html', context)



@login_required(login_url='signin')
def deleteLeave(request,pk):
    if request.method == 'POST':
        leave = LeaveMaster.objects.get(id = pk)
        leave.delete()
        messages.success(request,"Leave deleted Successfully")
        return redirect("leave-master")
        
    return render(request,'leave_master.html')

@login_required(login_url='signin')
def editLeave(request, pk):
    leave = get_object_or_404(LeaveMaster, id=pk)
    
    if request.method == 'POST':
        leave_name = request.POST.get('leave_name')
        leave_code = request.POST.get('leave_code')
        status = request.POST.get('status')  == 'on'
        paid = request.POST.get('paid') == 'on'
        
        leave.leave_name = leave_name
        leave.leave_code = leave_code
        leave.status = status
        leave.paid_leave = paid
        leave.save()
        messages.success(request, "Leave updated successfully.")
        return redirect('leave-master')

    
    return render(request, 'leave_master.html')



@login_required(login_url='signin')
def LeaveApplicationView(request):
    leave_applications = LeaveApplication.objects.all()
    branchs = Branch.objects.all()
    curr_year = datetime.date.today().year
    year_range = range(curr_year-15, curr_year + 1)

    # Filtering by month
    month = request.GET.get('month')
    if month:
       leave_applications = leave_applications.filter(from_date__month=month)

    # Filteing by year
    selected_year = request.GET.get('year')
    if selected_year:
        leave_applications = leave_applications.filter(from_date__year=selected_year)

    # Filtering by branch
    branch = request.GET.get('branch')
    if branch:
        leave_applications = leave_applications.filter(employee__branch__branch_name = branch)

    employee_name = request.GET.get('employee_name')
    employees=None
    if employee_name:
        employees = Employee.objects.filter(
         Q(first_name__icontains=employee_name) | Q(last_name__icontains=employee_name)
    )

    if employees:
        employee_ids = employees.values_list('id', flat=True)
        leave_applications = leave_applications.filter(employee__id__in=employee_ids)
    
    selected_status = request.GET.get('status')
    if selected_status:
        leave_applications = leave_applications.filter(status=selected_status)

    items_per_page = 5

    # Pagination
    paginator = Paginator(leave_applications, items_per_page)
    page = request.GET.get('page')

    try:
        leave_applications = paginator.page(page)
    except PageNotAnInteger:
        leave_applications = paginator.page(1)
    except EmptyPage:
        leave_applications = paginator.page(paginator.num_pages)


    context = {
        'leave_applications': leave_applications,
        'branchs': branchs,
        'curr_year': curr_year,
        'year_range': year_range,
        'selected_status': selected_status,
        'employee_name' : employee_name,
        'branch' : branch,
        'selected_year' :selected_year,
        'month' : month
    }

    return render(request, 'leave_applications.html', context)




@login_required(login_url='signin')
def approve_leave(request,pk):
    leave = get_object_or_404(LeaveApplication , id = pk)
    leave.status = "Approved"
    leave.save()
    messages.success(request, "Leave Approved successfully.")
    redirect_to = request.META.get('HTTP_REFERER', 'leave-applications')
    return redirect(redirect_to)

@login_required(login_url='signin')
def reject_leave(request,pk):
    leave = get_object_or_404(LeaveApplication , id = pk)
    leave.status = "Rejected"
    leave.save()
    messages.success(request, "Leave Rejected successfully.")
    redirect_to = request.META.get('HTTP_REFERER', 'leave-applications')
    return redirect(redirect_to)

@login_required(login_url='signin')
def delete_leave(request,pk):
    leave = get_object_or_404(LeaveApplication , id = pk)
    leave.delete()
    messages.error(request, "Leave deleted successfully.")
    redirect_to = request.META.get('HTTP_REFERER', 'leave-applications')
    return redirect(redirect_to)



@login_required(login_url='signin')
def DepartmentMaster(request):
    department_records = Department.objects.all()
    
    if request.method == 'POST':
        
        department_form = DepartmentMasterForm(data=request.POST)
        department_code = request.POST['department_code']
        dname = request.POST['department_name']
        departmentcode_exist = Department.objects.filter(department_code=department_code).exists() or  Department.objects.filter(department_name=dname).exists()

        if departmentcode_exist:
    
            messages.error(request, "Department name or code already Exists")
            return redirect('department-master')
        
        if department_form.is_valid():
            department_form.save()
            messages.success(request, "Department added successfully.")
            return redirect('branch-master')
    else:
        department_form = DepartmentMasterForm()

    context = {
        'department_records': department_records,
        'department_form': department_form,
    }
    return render(request, 'department_master.html', context)



@login_required(login_url='signin')
def deleteDepartment(request,pk):
    if request.method == 'POST':
        department = Department.objects.get(id = pk)
        department.delete()
        messages.success(request,"Department deleted Successfully")
        return redirect("department-master")
        
    return render(request,'department-master.html')

@login_required(login_url='signin')
def editDepartment(request, pk):
    department = get_object_or_404(Department, id=pk)
    
    if request.method == 'POST':
        department_name = request.POST.get('department_name')
        department_code = request.POST.get('department_code')
        status = request.POST.get('status')  == 'on'
        
        department.department_name = department_name
        department.department_code = department_code
        department.status = status
        department.save()
        messages.success(request, "Department updated successfully.")
        return redirect('department-master')

    
    return render(request, 'department-master.html')



def DesignationMaster(request):
    designation_records = Designation.objects.all()
    
    if request.method == 'POST':
        
        designation_form = DesignationMasterForm(data=request.POST)
        designation_code = request.POST['designation_code']
        dname = request.POST['designation_name']
        designationcode_exist = Designation.objects.filter(designation_code=designation_code).exists() or  Designation.objects.filter(designation_name=dname).exists()

        if designationcode_exist:
        
            messages.error(request, "Designation name or code already Exists")
            return redirect('designation-master')
        
        if designation_form.is_valid():
            designation_form.save()
            messages.success(request, "Designation added successfully.")
            return redirect('designation-master')
    else:
        designation_form = DesignationMasterForm()

    context = {
        'designation_records': designation_records,
        'designation_form': designation_form,
    }
    return render(request, 'designation_master.html', context)



@login_required(login_url='signin')
def deleteDesignation(request,pk):
    if request.method == 'POST':
        designation = Designation.objects.get(id = pk)
        designation.delete()
        messages.success(request,"Designation deleted Successfully")
        return redirect("designation-master")
        
    return render(request,'designation-master.html')

@login_required(login_url='signin')
def editDesignation(request, pk):
    designation = get_object_or_404(Designation, id=pk)
    
    if request.method == 'POST':
        designation_name = request.POST.get('designation_name')
        designation_code = request.POST.get('designation_code')
        status = request.POST.get('status')  == 'on'
        
        designation.designation_name = designation_name
        designation.designation_code = designation_code
        designation.status = status
        designation.save()
        messages.success(request, "Designation updated successfully.")
        return redirect('designation-master')

    
    return render(request, 'designation-master.html')


@login_required(login_url='signin')
def BranchMaster(request):
    branch_records = Branch.objects.all()
    
    if request.method == 'POST':
        
        branch_form = BranchMasterForm(data=request.POST)
        branch_code = request.POST['branch_code']
        branch_name = request.POST['branch_name']
        branchcode_exist = Branch.objects.filter(branch_code=branch_code).exists() or  Branch.objects.filter(branch_name=branch_name).exists()

        if branchcode_exist:
        
            messages.error(request, "Branch name or code already Exists")
            return redirect('branch-master')
        
        if branch_form.is_valid():
            branch_form.save()
            messages.success(request, "Branch added successfully.")
            return redirect('branch-master')
    else:
        branch_form = BranchMasterForm()

    context = {
        'branch_records': branch_records,
        'branch_form': branch_form,
    }
    return render(request, 'branch_master.html', context)



@login_required(login_url='signin')
def deleteBranch(request,pk):
    if request.method == 'POST':
        branch = Branch.objects.get(id = pk)
        branch.delete()
        messages.success(request,"Branch deleted Successfully")
        return redirect("branch-master")
        
    return render(request,'branch-master.html')

@login_required(login_url='signin')
def editBranch(request, pk):
    branch = get_object_or_404(Branch, id=pk)
    
    if request.method == 'POST':
        branch_name = request.POST.get('branch_name')
        branch_code = request.POST.get('branch_code')
        address = request.POST.get('address')
        tehsil = request.POST.get('tehsil')
        district = request.POST.get('district')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        status = request.POST.get('status')  == 'on'
        
        branch.branch_name = branch_name
        branch.branch_code = branch_code
        branch.address = address
        branch.tehsil = tehsil
        branch.district = district
        branch.city = city
        branch.state = state
        branch.country = country
        branch.status = status
        branch.save()
        messages.success(request, "Branch updated successfully.")
        return redirect('branch-master')

    
    return render(request, 'branch-master.html')


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, "You are not authorized to access this page.")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')



@login_required(login_url='signin')
def LogoutView(request):
    logout(request)
    return redirect('signin')



@login_required(login_url='signin')
def Dashboard(request):
    try:
        ec = Employee.objects.count()
    except:
        ec = 0
    context = {
        'ec' : ec,
    }
    return render(request,'dashboard.html' , context)


@login_required(login_url='signin')
def EmployeeView(request):
    employees = Employee.objects.all()
    branchs = Branch.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    numeric_part = 0

    # Handling GET request
    if request.method == 'GET':
        try:

            seleted_branch = request.GET.get('branch')
            if seleted_branch:
                employees = employees.filter(branch__branch_name=seleted_branch)
            
            employee_name = request.GET.get('employee_name')
            if employee_name:
                employees = employees.filter(Q(first_name__icontains=employee_name) | Q(last_name__icontains=employee_name))
            # Get the last employee code and extract numeric part for increment
            last_employee = Employee.objects.order_by('-employee_code').first()
            if last_employee:
                last_code = last_employee.employee_code
                if last_code and any(char.isdigit() for char in last_code):
                    numeric_part = int(''.join(filter(str.isdigit, last_code)))
        except Employee.DoesNotExist:
            pass  # Handle the case when no Employee objects exist
    
    items_per_page = 5

    # Pagination
    employees = employees.order_by('id')
    paginator = Paginator(employees, items_per_page)
    page = request.GET.get('page')

    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    
    
    # Create context for the form with necessary data
    context = {
        'employees': employees,
        'next_employee_code': numeric_part + 1,
        'designations': designations,
        'departments': departments,
        'branchs': branchs, 
        'selected_branch' : seleted_branch,
        'employee_name' : employee_name
    }
    
    return render(request, 'employee.html', context)


@login_required(login_url='signin')
def UserView(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        is_active = request.POST.get('is_active') == 'on'  # Convert checkbox value to boolean
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        if password == confirm_password:
            try:
                existing_user = User.objects.filter(username=username).exists()
                if existing_user:
                    messages.error(request, "Username already exists. Please choose a different username.")
                    return redirect('users')

                existing_email = User.objects.filter(email=email).exists()
                if existing_email:
                    messages.error(request, "Email already exists. Please choose a different email.")
                    return redirect('users')

                # Create and save the user object
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_active=is_active,
                    is_staff=is_staff,
                    is_superuser=is_superuser
                )
                if user:
                    user.save()
                    messages.success(request, "User added successfully.")
                    return redirect('users')
            except Exception as e:
                messages.error(request, f"Error creating user: {e}")
        else:
            messages.error(request, "Password and Confirm Password do not match")
            return redirect('users')
            
    users = User.objects.all()
    context = {'users' :  users}
    return render(request , 'users.html' , context)


@login_required(login_url='signin')
def editUserView(request,pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        try:
            existing_user = User.objects.exclude(id=user.id).filter(username=username).exists()
            if existing_user:
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('edit_user', user_id=user.id)

            existing_email = User.objects.exclude(id=user.id).filter(email=email).exists()
            if existing_email:
                messages.error(request, "Email already exists. Please choose a different email.")
                return redirect('edit_user', user_id=user.id)
        
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = is_active
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()

            messages.success(request, "User updated successfully.")
            return redirect('users')

        except Exception as e:
            messages.error(request, f"Error updating user: {e}")
            return redirect('edit_user', user_id=user.id)

    context = {'user': user}
    return render(request, 'users.html', context)


@login_required(login_url='signin')
def deleteUser(request,pk):
    if request.method == 'POST':
        user = User.objects.get(id = pk)
        if user:
            user.delete()
            messages.success(request,"User is deleted Successfully")
            return redirect("users")
        
    return render(request,'users.html')


@login_required(login_url='signin')
def deleteEmployee(request,pk):
    if request.method == 'POST':
        employee = Employee.objects.get(id = pk)
        if employee:
            employee.delete()
            messages.success(request,"Employee deleted successfully..")
            return redirect("employees")
    return render(request,'employee.html')


@login_required(login_url='signin')
def deleteDocument(request,pk1,pk2):
    if request.method == 'POST':
        if 'required_documents' in request.POST:
            document = RequiredDocument.objects.get(id=pk2)
            if document:
                document.delete()
                messages.success(request,"Document deleted successfully..")
                return redirect("employee_profile",pk=pk1)
            
        if 'immigration_documents' in request.POST:
            document = Immigration.objects.get(id=pk2)
            if document:
                document.delete()
                messages.success(request,"Document deleted successfully..")
                return redirect("employee_profile",pk=pk1)
            
        if 'bank_record' in request.POST:
            document = BankDetails.objects.get(id=pk2)
            if document:
                document.delete()
                messages.success(request,"Bank details deleted successfully..")
                return redirect("employee_profile",pk=pk1)
            
    return render(request,'employee_profile.html')



@login_required(login_url='signin')
def employeeProfileView(request , pk):
    employee = Employee.objects.get(id = pk)
    immigration_form = None
    bank_form = None
    document_form=None
    form = None
    emp_code = None
    emp_branch_code = None
    if employee.employee_code:
        temp = employee.employee_code.split('/')
        emp_branch_code = f"{temp[0]}/{temp[1]}"
        emp_code = temp[2]

        
    if request.method == 'POST':
        # Extracting data from the POST request
        if 'personal_information' in request.POST:
            personal_info, created = PersonalInformation.objects.get_or_create(employee=employee)
            form = PersonalInformationForm(request.POST,instance=personal_info)

            if form.is_valid():
                form.save()
                messages.success(request,"Updated Successfully..")
                return redirect('employee_profile',pk=employee.id)
            else:
                messages.error(request,"Something went wrong....")
        
        if 'general_information' in request.POST:
            
            
            official_email = request.POST.get('official_email')
            
            official_email_exist = Employee.objects.filter(official_email=official_email)
           
            if  official_email_exist and official_email!= employee.official_email:
                messages.error(request,"Employee is already reistered with this email...")
                return redirect('employee_profile',pk=employee.id)
            else:
                
                employee.official_email = official_email
            
            employee.middle_name = request.POST.get('middle_name')
            
            employee.gender = request.POST.get('gender')
            branch_id = request.POST.get('branch')
        
            branch = get_object_or_404(Branch, id=branch_id)
        
            employee.branch = branch
            branch_code = request.POST.get('branch_code')
            code = request.POST.get('code')
            employee.employee_code = f"{branch_code}/{code}"
        
            punching_code = request.POST.get('punching_code')
            punching_code_exist = Employee.objects.exclude(id=employee.id).filter(punching_code=punching_code)

            if punching_code_exist.exists():
                messages.error(request, "Punching code is already in use.")
                return redirect('employee_profile', pk=employee.id)
            else:
                employee.punching_code = punching_code
            department_id = request.POST.get('department')
            department = get_object_or_404(Department, id=department_id)
            employee.department = department
            designation_id = request.POST.get('designation')
            designation = get_object_or_404(Designation, id=designation_id)
            employee.designation = designation
            employee.date_of_joining = request.POST.get('doj')
            employee.employee_type = request.POST.get('employee_type')
            employee.shift = request.POST.get('shift')
            employee.grade = request.POST.get('grade')
            reporting_manager_id = request.POST.get('reporting_manager')
            if reporting_manager_id:
                reporting_manager = get_object_or_404(Employee,id=reporting_manager_id)
                employee.reporting_manager = reporting_manager
            employee.ctc = request.POST.get('ctc')
            employee.basic_salary = request.POST.get('basic_salary')
            employee.gross_salary = request.POST.get('gross_salary')

            employee.save()
            messages.success(request,"Updated sucessfully..")
            return redirect('employee_profile',pk=employee.id)
        
        if 'documents' in request.POST:

            document_form = DocumentForm(request.POST, request.FILES)
            if document_form.is_valid():
                document = document_form.save(commit=False)
                document.employee = employee
                document_form.save()
                messages.success(request,"Document uploaded successfully..")
                return redirect('employee_profile',pk=employee.id)
            else:
                messages.error(request,"Something went wrong....")
        
        if 'immigration' in request.POST:

            immigration_form = ImmigrationForm(request.POST, request.FILES)
            if immigration_form.is_valid():
                document = immigration_form.save(commit=False)
                document.employee = employee
                immigration_form.save()
                messages.success(request,"Immigration details added successfully..")
                return redirect('employee_profile',pk=employee.id)
            else:
                messages.error(request,"Something went wrong....")
        
        if 'bank_details' in request.POST:

            bank_form = BankForm(request.POST)
            other_bank_name = request.POST.get('bank_name_other')
    
            if bank_form.is_valid():
                document = bank_form.save(commit=False)
                if document.bank_name == "Other":
                    document.bank_name = other_bank_name
                document.employee = employee
                bank_form.save()
                messages.success(request,"Bank details added successfully..")
                return redirect('employee_profile',pk=employee.id)
            else:
                messages.error(request,"Something went wrong....")

    employees_list = Employee.objects.all()
    branchs = Branch.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    numeric_part = 0
    employee_documents = None
    

    # Handling GET request
    if request.method == 'GET':
        personal_info, created = PersonalInformation.objects.get_or_create(employee=employee)
        employee_documents= RequiredDocument.objects.filter(employee=employee)
        immigration_documents = Immigration.objects.filter(employee=employee)
        leaves_applications = LeaveApplication.objects.filter(employee=employee)
        bank_records = BankDetails.objects.filter(employee=employee)
        form = PersonalInformationForm(instance=personal_info)
        document_form = DocumentForm()
        immigration_form = ImmigrationForm()
        bank_form = BankForm()
        try:
            # Get the last employee code and extract numeric part for increment
            last_employee = Employee.objects.order_by('-employee_code').first()
            if last_employee:
                last_code = last_employee.employee_code
                if last_code and any(char.isdigit() for char in last_code):
                    numeric_part = int(''.join(filter(str.isdigit, last_code)))
        except Employee.DoesNotExist:
            pass  # Handle the case when no Employee objects exist
    
    # Create context for the form with necessary data
    
    
    context = {
        'employee': employee,
        'emp_branch_code' : emp_branch_code,
        'emp_code' : emp_code,
        'next_employee_code': numeric_part + 1,
        'designations': designations,
        'departments': departments,
        'branchs': branchs, 
        'employees_list' : employees_list,
        'form' : form,
        'document_form' : document_form,
        'immigration_form' : immigration_form,
        'employee_documents' : employee_documents,
        'immigration_documents': immigration_documents,
        'bank_form' : bank_form,
        'bank_records' : bank_records,
       
    }
    return render(request,'employee_profile.html',context)




def handler404(request,exception):
    return render(request,'404.html')

def handler500(request):
    return render(request,'500.html')
    



