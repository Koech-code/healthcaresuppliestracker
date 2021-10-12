from django.shortcuts import render
from rest_framework import generics, serializers,status, views, permissions
from rest_framework_simplejwt.state import User
from . serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, ResetPasswordSerializer, ItemSerializer, HospitalSerializer, StatuSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, Token
from .utils import Mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly
from .models import Hospital, Item
from django.http import Http404
# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer

    def post(self, request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user=User.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token
        
        email_body='Hi '+user.name+' welcome to our Health Care Supplies Tracker application.'

        data={'email_body':email_body, 'to_email':user.email, 'email_subject': 'Welcome'}
        Mail.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED )

class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
       
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
   

        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class=LogoutSerializer
    permission_classes=(permissions.IsAuthenticated,)

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ResetPasswordView(generics.GenericAPIView):

    serializer_class=ResetPasswordSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        email=request.data['email']

        if User.objects.filter(email=email).exists():
        
            user=User.objects.get(email=email)
            userid64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(request=request).domain
            relativeLink=reverse('reset-password', kwargs={'userid64':userid64, 'token':token})
            absolute_url='http://'+current_site+relativeLink

            email_body='Hello, \n use this link to reset your password \n'+absolute_url
            data={'email_body':email_body, 'to_email':user.email, 'email_subject':'Reset your password'}

            Mail.send_email(data)


        return Response({'success':'An email to reset your password has been sent to you.'}, status=status.HTTP_200_OK)

# class PasswordTokenCheckView(generics.GenericAPIView):
#     def get(self, request, userid64, token):
#         pass


class StatusView(generics.GenericAPIView):
    serializer_class=StatuSerializer

    def post(self, request):
        status=request.data
        serializer=self.serializer_class(data=status)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        
        return Response(user_data )

        
class ItemView(generics.GenericAPIView):
    serializer_class=ItemSerializer

    def post(self, request):
        status=request.data
        serializer=self.serializer_class(data=status)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        
        return Response(user_data )


class ItemList(APIView):
    def get(self, request,id, format=None):
        all_items = Item.objects.filter(id=id)
        serializers = ItemSerializer(all_items, many=True)
        return Response(serializers.data)

class HospitalView(generics.GenericAPIView):
    serializer_class=HospitalSerializer

    def post(self, request):
        status=request.data
        serializer=self.serializer_class(data=status)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        
        return Response(user_data )

class HospitaList(APIView):
    def get(self, request,id, format=None):
        all_hospitals = Hospital.objects.filter(id=id)
        serializers = HospitalSerializer(all_hospitals, many=True)
        return Response(serializers.data)



# class SingleHospital(APIView):
#     permission_classes=(IsAdminOrReadOnly,)
    
#     def get_hospital(self, pk):
#         try:
#             return Hospital.objects.get(pk=pk)
#         except Hospital.DoesNotExist:
#             return Http404
        
#     def get(self, request, pk, format=None):
#         merch=self.get_hospital(pk)
#         serializers=HospitalSerializer(merch)

#         return Response(serializers.data)