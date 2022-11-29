from .models import *
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from .forms import *
from .decorators import user_not_authenticated
from .tokens import account_activation_token


def profile(request):
    dom=Domaine.objects.all()
    form=ProfileForm()
    if request.method=="POST":
        form=ProfileForm(request.POST)
        if form.is_valid():
            Condidat.objects.create(user=request.user,age=form.cleaned_data['age'],phone=form.cleaned_data['phone'],location=form.cleaned_data['location'],gender=form.cleaned_data['gender'],profession=form.cleaned_data['profession'])
            return redirect("employment:home")
    return render(request,'profile.html',{"form":form,"dom":dom})

#redirect to homepage
def home(request):
    page="5"
    dom=Domaine.objects.all()
    if request.user.is_authenticated:
        page="1"
        print(request.user)
        user=User.objects.get(username=request.user)
        print(user.username)
        try:
            print(user.username)
            condidat=Condidat.objects.get(user=user)
            page="0"
        except:
            pass
        if page=="0":
            dom=Domaine.objects.all()
            return render(request,'index.html',{"dom":dom})
        else:
            return redirect("employment:profile")

    return render(request,'index.html',{"dom":dom})

#activate account user
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "please complete your profile information !")
        return redirect('employment:profile')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('employment:home')


#send email verification
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user} , please go to you email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

#user registration
@user_not_authenticated
def register(request):
    dom=Domaine.objects.all()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('employment:register')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegisterForm()

    return render(
        request=request,
        template_name="registration/register.html",
        context={"form": form,"dom":dom}
        )


def test(request,pk):
    dom=Domaine.objects.all()
    test=Test.objects.all()
    assoc=AssociatDomaineParCategory.objects.filter(domaine__id=pk)
    print(assoc)
    print(test)
    return render(request,'tests.html',{"test":test,"assoc":assoc,"dom":dom})

@login_required(login_url="login")
def affiche_test(request,pk):
    dom=Domaine.objects.all()
    test=Test.objects.get(id=pk)
    quiz=test.quiz_set.all()
    if request.method=="POST":
        sum=0
        avg=0
        for q in quiz :
            r1=request.POST.get(q.radio_name)
            avg=int(avg)+int(q.score)
            if r1==q.reponse :
                sum=int(sum)+int(q.score)
        return render(request,"result_test.html",{"sum":sum,"avg":avg,"dom":dom})

    return render(request,'affiche_test.html',{"quiz":quiz,"dom":dom})
