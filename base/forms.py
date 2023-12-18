from django import forms
from .models import *
import string , re
from django.forms import DateInput,FileInput
from .constants import STATE_CHOICES


class HolidayMasterForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'holiday_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=STATE_CHOICES , attrs={'class': 'form-control'}),
            'branch' : forms.Select(attrs={'class': 'form-control'}),
            'holiday_date' : forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'holiday_category': forms.Select(choices=Holiday.HOLIDAY_CHOICES , attrs={'class': 'form-control'}),
        }


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
            'blood_group': forms.Select(choices=PersonalInformation.BLOOD_GROUP_CHOICES , attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'cast_category': forms.Select(choices=PersonalInformation.CASTE_CATEGORY_CHOICES,attrs={'class': 'form-control'}),
            'marital_status': forms.Select(choices=PersonalInformation.MARITAL_STATUS_CHOICES,attrs={'class': 'form-control'}),
            'aadhaar_card_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pancard_no': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'tehsil': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=STATE_CHOICES , attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        special_characters = set(string.punctuation)

        mobile_no = cleaned_data.get('mobile_no')
        if mobile_no:
            if not mobile_no.isdigit() or len(mobile_no) != 10:
                self.add_error("mobile_no", "Mobile Number should contain exactly 10 digits and only numeric characters")

        pincode = cleaned_data.get('pincode')
        if pincode:
            if not pincode.isdigit() or len(pincode) != 6:
                self.add_error("pincode", "Pincode should contain exactly 6 digits and only numeric characters")

        aadhaar_card_no = cleaned_data.get('aadhaar_card_no')
        if aadhaar_card_no:
            if not aadhaar_card_no.isdigit() or len(aadhaar_card_no) != 12:
                self.add_error("aadhaar_card_no", "Aadhaar Number should contain exactly 12 digits and only numeric characters")

        pancard_no = cleaned_data.get('pancard_no')
        if pancard_no:
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pancard_no):
                self.add_error("pancard_no", "Enter a valid PAN card number (e.g., ABCDE1234F)")

            if len(pancard_no) != 10:
                self.add_error("pancard_no", "Pancard Number should contain exactly 10 digits")
        

        fields_to_check = [
            'father_name',
            'mother_name',
            'city',
            'country',
            'nationality',
            'cast_category',
            'district',
            'tehsil',
        ]

        for field in fields_to_check:
            field_value = cleaned_data.get(field)
            if field_value:
                # Check for numeric or special characters
                if any(char.isdigit() or char in special_characters for char in field_value):
                    self.add_error(field, f"{field.replace('_', ' ').capitalize()} should not contain numeric or special characters.")
        
        return cleaned_data
