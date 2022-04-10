from django.shortcuts import render, redirect, reverse, Http404

from django.views.generic import View

from django.core.mail import send_mail

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserExtendsForm, UserProfileForm, EditUserForm
from .utils import token_generator
from .models import UserProfile

from articles.models import Article

from django.contrib import messages

from django.conf import settings


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserExtendsForm()
        profile_form = UserProfileForm()

        if request.method == 'POST':
            form = UserExtendsForm(request.POST)
            profile_form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid() and profile_form.is_valid():
                
                user = form.save()

                user.is_active=False

                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                profile.save()

                uidb64 = urlsafe_base64_encode( force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64': uidb64,
                    'token': token_generator.make_token(user)
                })

                activate_url = 'http://' + domain + link

                email_subject = 'Activate your account on BlogIt'
                email_body = 'Hi there ' + user.username + '! Welcome to BlogIt app... \n \n Please verify your email by following this link: ' + activate_url
                recipient = str(form['email'].value())

                email = send_mail(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [recipient,],
                    fail_silently=False
                )

                return redirect('activate-user')
        else:
            form = UserExtendsForm()
            profile_form = UserProfileForm()

        context = {
            'form': form,
            'profile_form': profile_form,
        }

        return render(request, 'accounts/register.html', context)

def activateUser(request):
    return render(request, 'accounts/activate.html', context={})


class VertificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if user.is_active:
                return redirect('login')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Account was activated for: ' + user.username)
                return redirect('login')

        except Exception as e:
            messages.error(request, 'There was an error activating your account, ' + e)
            return redirect('login')

        return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Username or Password is incorrect!')
                return redirect('login')

        context = {}

        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('index')

def userProfile(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        articles = Article.objects.filter(user=user_profile).count()
    else:
        return Http404()

    context = {
        'user': user_profile,
        'articles': articles,
    }
    return render(request, 'accounts/user-profile.html', context)


def userUpdate(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = EditUserForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect('/accounts/profile')
        else:
            form = EditUserForm(instance=request.user)
            profile_form = UserProfileForm(instance=user_profile)
    else:
        return Http404()
    
    context = {
        'user': user_profile,
        'form': form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/update-user.html', context)

def userUpdatePassword(request):
    user_profile = ''
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/accounts/profile')
        else:
            form = PasswordChangeForm(user=request.user)

    context = {
        'user': user_profile,
        'form': form,
    }

    return render(request, 'accounts/update-user-password.html', context)
