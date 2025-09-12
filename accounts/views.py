from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserEditForm,UserProfileForm
from .tokens import account_activation_token
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from blog.models import Post
from .models import Profile
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
 


@ login_required
def favourite_list(request):
    new = Post.newmanager.filter(favourites=request.user)
    return render(request,
                  'accounts/favourites.html',
                  {'new': new})
    
    
@ login_required
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    referer = request.META.get('HTTP_REFERER', '/')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()}):
        return HttpResponseRedirect(referer)
    return HttpResponseRedirect('/')


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {
            "avatar": avatar,
        }
        return context
    else:
        return {
            'NotLoggedIn': User.objects.none()
        }


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'section': 'profile'})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request,
                  'accounts/update.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.is_active = False
        user.save()
        return redirect('userauth:login')
    return render(request, 'accounts/delete.html')


def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('Registered successfully. Activation email sent.')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('userauth:profile')
    else:
        return render(request, 'registration/activation_invalid.html')


@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('userauth:password_change_done')  # 👈 Redirect here
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

