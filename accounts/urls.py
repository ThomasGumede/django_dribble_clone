from django.urls import path
from .forms import UserLoginForm
from .views import (
    SignUpView, 
    PwdResetConfirmView, 
    AccountDetailsView, 
    EditProfileView, 
    GeneralView, 
    UpdatePasswordView,
    PwdResetView,
    AccountLikesView
)
from django.contrib.auth.views import (
    LoginView, 
    LogoutView,   
)

app_name = 'accounts'

urlpatterns = [
    
    path('login', LoginView.as_view(template_name='accounts/login.html', form_class=UserLoginForm, redirect_authenticated_user=True), name='login'),
    path('logout', LogoutView.as_view(next_page="shots:shot_list"), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path("password", UpdatePasswordView.as_view(), name="password_change"),
    path('password/reset_password', PwdResetView.as_view(), name='password_reset'),
    path('<username>/<pk>', AccountDetailsView.as_view(), name='user_details'),
    path("likes/<username>/<pk>", AccountLikesView.as_view(), name="liked_shots"),
    path('update/<username>/<pk>', EditProfileView.as_view(), name='account_update'),
    path('general/<username>/<pk>', GeneralView.as_view(), name='general_edit'),
    path('password/<uidb64>/<token>', PwdResetConfirmView.as_view(), name='pwd_reset_confirm'),
    
]