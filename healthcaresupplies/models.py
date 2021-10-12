from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class UserManager(BaseUserManager):

    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
  
    def create_user(self, name, email, location, phone_number, password=None):

        """
        Create and return a `User` with an email, name,location, phone_number and password.
        """

        if name is None:
            raise TypeError('Users should have a name.')
        if email is None:
            raise TypeError('Users should have an email.')
        if location is None:
            raise TypeError('Users should have a location.')
        if phone_number is None:
            raise TypeError('Users should have phone_number.')

        user=self.model(name=name, email=self.normalize_email(email), phone_number=phone_number, location=location)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, name,email,phone_number, location, password=None):
        
        """
        Create and return a `User` with superuser (admin) permissions.
        """

        if password is None:
            raise TypeError('This field should not be none.')
        if email is None:
            raise TypeError('Users should have an email.')
        if location is None:
            raise TypeError('Users should have a location.')
        if phone_number is None:
            raise TypeError('Users should have phone_number.')
        
        user=self.create_user(name,phone_number, location, email, )
        user.is_superuser=True
        user.is_staff=True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    name=models.CharField(max_length=30, unique=True, db_index=True)
    email=models.EmailField(max_length=60, unique=True, db_index=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    phone_number=models.IntegerField(default=0)
    location=models.CharField(max_length=60, default='no location')
    is_active=models.BooleanField(default=True)
    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_staff=models.BooleanField(default=False)
    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    created_at=models.DateField(auto_now_add=True)
    # A timestamp representing when this object was created.
    updated_at=models.DateField(auto_now=True)
    # A timestamp representing when this object was last updated.

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']
    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.

    objects=UserManager()
    # Tells Django that the UserManager class defined above should manage
    # objects of this type.

    def __str__(self):
        return self.email
        
    """
    Returns a string representation of this `User`.

    This string is used when a `User` is printed in the console.
    """

    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }


class Status(models.Model):
    status=models.CharField(max_length=10, default='no status')

    def __str__(self):
        return self.status

    
class Donor(models.Model):
    name=models.CharField(max_length=30, default='no name')
    email=models.EmailField(max_length=60, default=0)
    phone_number=models.IntegerField(default=0)
    location=models.CharField(max_length=60, default='no location')
    
class Hospital(models.Model):
    name=models.CharField(max_length=30, default='no name')
    email=models.EmailField(max_length=60, default=0)
    phone_number=models.IntegerField(default=0)
    location=models.CharField(max_length=60, default='no location')

class Item(models.Model):
    item_name=models.CharField(max_length=30, default='no data')
    quantity=models.IntegerField( default=0)
    description=models.TextField(max_length=255, default='no data')
    order_status=models.ForeignKey(Status, max_length=10, default='no status', on_delete=models.CASCADE)
    donor=models.ForeignKey(Donor, max_length=10, null=True,  on_delete=models.CASCADE)
    hospital=models.ForeignKey(Hospital, max_length=10, null=True, on_delete=models.CASCADE)