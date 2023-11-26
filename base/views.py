
from .models import PersonalInformation,Employee,Branch,Department,Designation,RequiredDocument
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from .forms import PersonalInformationForm,DocumentForm



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
    return render(request,'dashboard.html')


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
        'employees': employees,
        'next_employee_code': numeric_part + 1,
        'designations': designations,
        'departments': departments,
        'branchs': branchs, 
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
def deleteEmployeeDocument(request,pk1,pk2):
    if request.method == 'POST':
        document = RequiredDocument.objects.get(id=pk2)
        if document:
            document.delete()
            messages.success(request,"Document deleted successfully..")
            return redirect("employee_profile",pk=pk1)
    return render(request,'employee_profile.html')



@login_required(login_url='signin')
def employeeProfileView(request , pk):
    employee = Employee.objects.get(id = pk)
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
            email = request.POST.get('email')
            
            official_email = request.POST.get('official_email')
            
            official_email_exist = Employee.objects.filter(official_email=official_email)
            email_exist = Employee.objects.filter(email=email)
            if email_exist and email != employee.email  or official_email_exist and official_email!= employee.official_email:
                messages.error(request,"Employee is already reistered with this email...")
                return redirect('employee_profile',pk=employee.id)
            else:
                employee.email = email
                employee.official_email = official_email
            employee.first_name = request.POST.get('first_name')
            employee.middle_name = request.POST.get('middle_name')
            employee.last_name = request.POST.get('last_name')
            employee.gender = request.POST.get('gender')
            branch_id = request.POST.get('branch')
            # print(branch_id)
            branch = get_object_or_404(Branch, id=branch_id)
            print(branch)
            employee.branch = branch
            branch_code = request.POST.get('branch_code')
            code = request.POST.get('code')
            employee.employee_code = f"{branch_code}/{code}"
            # print(employee.employee_code)
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
        form = PersonalInformationForm(instance=personal_info)
        document_form = DocumentForm()
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
        'employee_documents' : employee_documents
    }
    return render(request,'employee_profile.html',context)




def handler404(request,exception):
    return render(request,'404.html')

def handler500(request):
    return render(request,'500.html')
    



