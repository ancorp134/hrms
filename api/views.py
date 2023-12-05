from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from base.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

class EmployeeLoginView(APIView):
    def post(self, request):
        serializer = EmployeeLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = Employee.objects.get(user=request.user)
        bank_details = BankDetails.objects.filter(employee=employee)
        bank_data = BankDetailsSerializer(bank_details,many=True)  
        serializer = EmployeeSerializer(employee)
        return Response({
            "employee": serializer.data,

            "bank_details": bank_data.data  # accessing the serialized data
        })
    
class EmployeeAttendence(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            # Get the employee associated with the authenticated user
            employee = Employee.objects.get(user=request.user)
            
            # Include employee ID in the data sent for serializer validation
            data = request.data.copy()
            data['employee'] = employee.id  # Assuming 'employee' is the ForeignKey in EmployeeAttendance
        
            serializer = AttendanceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
class LeaveApplicationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes  = [JSONParser]

    def get(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
            leave_applications = LeaveApplication.objects.filter(employee__reporting_manager=employee)
            
            # Serialize the queryset using the serializer
            serializer = LeaveApplicationSerializer(leave_applications, many=True)
            
            return Response({
                "leave_approvals": serializer.data  # Return serialized data
            })
        except Employee.DoesNotExist:
            return Response({
                "status": "No data is available"
            })


    def post(self,request):
        try:
            employee = Employee.objects.get(user = request.user)
            data = request.data.copy()
            data['employee'] = employee.id 

            serializer = LeaveApplicationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)



