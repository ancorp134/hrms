from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from base.models import *
from rest_framework.permissions import IsAuthenticated

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
