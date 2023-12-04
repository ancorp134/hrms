from django import forms
from .models import *
import string
from django.forms import DateInput,FileInput
from .constants import STATE_CHOICES


class LeaveMasterForm(forms.ModelForm):
    class Meta:
        model =  LeaveMaster
        fields = '__all__'
        widgets = {
            'leave_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'leave_code' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class DesignationMasterForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'
        widgets = {
            'designation_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'designation_code' : forms.TextInput(attrs={'class': 'form-control'}),
        }


class DepartmentMasterForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'department_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'department_code' : forms.TextInput(attrs={'class': 'form-control'}),
        }


class BranchMasterForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
        widgets = {
            'branch_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'branch_code' : forms.TextInput(attrs={'class': 'form-control'}),
            'address' : forms.TextInput(attrs={'class': 'form-control'}),
            'tehsil' : forms.TextInput(attrs={'class': 'form-control'}),
            'district' : forms.TextInput(attrs={'class': 'form-control'}),
            'city' : forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=STATE_CHOICES , attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            

        }


class BankForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        exclude = ('employee',)
        fields = '__all__'
        widgets = {
            'bank_name': forms.Select(choices=BankDetails.BANK_CHOICES, attrs={'class': 'form-control','id' : 'id_bank_name'}),
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'IFSC_code': forms.TextInput(attrs={'class': 'form-control'}),
            'branch_name': forms.TextInput(attrs={'class': 'form-control'}),
            'branch_address': forms.TextInput(attrs={'class': 'form-control'}),
          
        }

class ImmigrationForm(forms.ModelForm):
    class Meta:
        model = Immigration
        exclude = ('employee',)
        fields = '__all__'
        widgets = {
            'document_type': forms.Select(choices=Immigration.IMMI_CHOICES, attrs={'class': 'form-control'}),
            'passport_or_visa_no': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'citizenship': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),

        }


class DocumentForm(forms.ModelForm):
    

    class Meta:
        model = RequiredDocument
        exclude = ('employee',)
        fields = '__all__'
        widgets = {
            'document_type' : forms.Select( choices=RequiredDocument.DOCUMENT_CHOICES,attrs={'class' : 'form-control'}),
            'document' : forms.FileInput(attrs={'class' : 'form-control'}),
            'date_of_expiry': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comments' : forms.Textarea(attrs={'class' : 'form-control', 'rows': 3, 'cols': 40}),
        }
    def clean_document(self):
        document = self.cleaned_data['document']
        if document:
            content_type = document.content_type
            if content_type != 'application/pdf':
                raise forms.ValidationError("Only PDF files are allowed.")
        return document
    



class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = '__all__'
        widgets = {
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'tehsil': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'cast_category': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=STATE_CHOICES , attrs={'class': 'form-control'}),
            'blood_group': forms.Select(choices=PersonalInformation.BLOOD_GROUP_CHOICES , attrs={'class': 'form-control'}),
        }

    def clean(self):
        
       
        cleaned_data = super().clean()
        special_characters = set(string.punctuation)

        fields_to_check = [
            'father_name',
            'mother_name',
            'city',
            'country',
            'nationality',
            'cast_category',
            
        ]

        for field in fields_to_check:
            field_value = cleaned_data.get(field)
            
            if field_value:
                # Check for numeric or special characters
                if any(char.isdigit() or char in special_characters for char in field_value):
                    self.add_error(field, f"{field.replace('_', ' ').capitalize()} should not contain numeric or special characters.")
                
                # Additional specific validations (e.g., pincode length)
                if field == 'pincode':
                    if not field_value.isdigit() or len(field_value) != 6:
                        self.add_error(field, "Please enter a valid 6-digit pincode.")
                
                # Check mobile number length
                if field == 'mobile_no':
                    cleaned_mobile_number = ''.join(filter(str.isdigit, field_value))
                    if len(cleaned_mobile_number) != 10:
                        self.add_error(field, "Mobile number should be exactly 10 digits long.")

        return cleaned_data
