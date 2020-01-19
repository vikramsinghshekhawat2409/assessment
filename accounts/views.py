from django.shortcuts import render
from accounts.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    """
    :param request:
    :return: returns rendered html template with welcome message including an username if the user is logged in
             and if not so returns rendered html asking user to register or log in
             and if any exception raises returns an internal server error with the error
    """
    try:
        return render(request,'accounts/index.html')
    except Exception as e:
        return HttpResponse(e, status=500)

@login_required
def special(request):
    """
    @login_required will redirect user to settings.redirect_url if a user is not logged in
                                                                else will execute the flow normally
    :param request:
    :return: returns logged in response
    """
    try:
        return HttpResponse("You are logged in !")
    except Exception as e:
        return HttpResponse(e, status=500)


@login_required
def user_logout(request):
    """
    performs logout request
    :param request:
    :return: redirect user to url pattern name index in the url.py file
    """
    try:
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    except Exception as e:
        return HttpResponse(e, status=500)


def signup(request):
    """
    performs registration of the user through forms
    :param request: includes user attributes from user form i.e first_name, last_name, email, password
    :return: returns the success if the user is registered successfully and forms is valid else returns to the user form
    """
    try:
        registered = False
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            user_form.username = request.POST['email']
            profile_form = UserProfileInfoForm(data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = User()
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.username = request.POST.get('email')
                user.set_password(request.POST.get('password'))
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True
            else:
                print(user_form.errors,profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = UserProfileInfoForm()
        return render(request,'accounts/registration.html',
                              {'user_form':user_form,
                               'profile_form':profile_form,
                               'registered':registered})
    except Exception as e:
        return HttpResponse(e, status=500)


def user_login(request):
    """
    performs the users login request
    :param request: includes the user attributes which contains email and password
    :return: if the user's credentials are correct and the user is active returns a welcome message with user's email
             elif user's account is inactive then returns an inactive account message
             else error message is returned with an tried to login other's account
    """
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return HttpResponse("Invalid login details given")
        else:
            return render(request, 'accounts/login.html', {})
    except Exception as e:
        return HttpResponse(e, status=500)
