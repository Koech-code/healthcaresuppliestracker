from django.contrib import auth
from django.db.models import fields
from django.http import request
from rest_framework import generics, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.fields import ReadOnlyField
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from .models import User, Donor,Hospital, Status, Item
from django.http import Http404
class RegisterSerializer(serializers.ModelSerializer):

    """
    Serializers registration requests and creates a new user.
    """

    password=serializers.CharField(max_length=50, min_length=8, write_only=True)

    # Ensure passwords are at least 8 characters long, no longer than 50
    # characters, and can not be read by the client.

    class Meta:
        model=User
        # List all the fields that could possibly be included in a request
        # or response, including fields specified explicitly below.
        fields=['id','name', 'email', 'phone_number', 'location', 'password']
    
    def validate(self, attrs):
        email=attrs.get('email', '')
        username=attrs.get('username', '')

        if not username.isalnum:
            raise serializers.ValidationError('The username should only contain alphanumeric characters')

        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

        # Use the `create_user` method we wrote earlier to create a new user.


class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=50, min_length=8, write_only=True)
    email=serializers.EmailField(max_length=60, min_length=5)
    name=serializers.CharField(max_length=30, min_length=3, read_only=True)

    tokens=serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user=User.objects.get(email=obj['email'])

        return {
            'refresh_key':user.tokens()['refresh'],
            'access_key':user.tokens()['access'],
        }
        
    class Meta:
        model=User
        fields=['email', 'password', 'name', 'tokens']

    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')
        user=auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')

        return {
            'email':user.email,
            'name':user.name,
            'tokens':user.tokens,

        }
class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()
    default_error_messages={
        'bad_token':'Your token has expired or is no longer valid.'

     }

    def validate(self, attrs):
        self.token=attrs['refresh']
        return attrs


    def save(self, **kwargs):
       
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ResetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=4)
    class Meta:
   
        fields=['email']


class StatuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields=['status']

    def validate(self, attrs):
        status=attrs.get('status', '')

        if not status.isalpha:
            raise serializers.ValidationError('Only alphabets are required')

        return attrs

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['id','item_name', 'quantity', 'description', 'order_status']

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hospital
        fields=['id','name', 'email', 'phone_number', 'location']



