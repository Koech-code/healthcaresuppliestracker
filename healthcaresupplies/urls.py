from django.conf.urls import url
from . views import HospitaList, RegisterView, LoginView, LogoutView, ResetPasswordView,StatusView, ItemView, HospitalView
from rest_framework_simplejwt.views import (TokenRefreshView,)
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns=[
    url('register/', RegisterView.as_view(), name='register'),
    url('login/', LoginView.as_view(), name='login'), 
    url('logout/', LogoutView.as_view(), name='logout'), 
    url('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('reset-password-email/',ResetPasswordView.as_view(), name='reset-password-email'), 
    url('status/', StatusView.as_view(), name='status'),
    url('item/', ItemView.as_view(), name='item'),
    url('items/(\d+)', views.ItemList.as_view(), name='items'),
    url('hospital/', HospitalView.as_view(), name='hospital'),
    url('hospitals/(\d+)', views.HospitaList.as_view(), name='hospitals'),
    # url('reset-password/<userid64>/<token>/', PasswordTokenCheckView.as_view(), name='reset-password'),
    # url(r'api/hospital/hospital-id/(?P<pk>[0-9]+)/$',views.SingleHospital.as_view())    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
