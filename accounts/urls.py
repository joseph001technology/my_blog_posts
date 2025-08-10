from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm, PwdChangeForm
from django.urls import reverse_lazy
 

app_name = 'userauth'   

urlpatterns = [
    path(
        'password_change/',
        views.custom_password_change,
        name='pwdforgot'
    ),  # 👈 Use custom view

    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name='password_change_done'
    ),
    
    path(
        'signup/',
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
        ),
        name='custom_signup'
    ),

    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            form_class=PwdResetForm,
            success_url=reverse_lazy('userauth:password_reset_done')
        ),
        name='pwdreset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ), 
        name='password_reset_done'
    ),

    path('profile/', views.profile, name='profile'),

    path(
        'password_reset_confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            form_class=PwdResetConfirmForm,
            success_url=reverse_lazy('userauth:password_reset_complete')
        ),
        name="pwdresetconfirm"
    ),
    path(
    'password-reset/complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ),
    name='password_reset_complete'
),


    path('profile/edit/', views.edit, name='edit'),
    path('profile/delete/', views.delete_user, name='deleteuser'),
    path('register/', views.accounts_register, name='register'),
    path(
        'activate/<slug:uidb64>/<slug:token>/',
        views.activate,
        name='activate'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
