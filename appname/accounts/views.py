from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,View,TemplateView,DeleteView,ListView
from. import models
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from . import forms

#...
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from difflib import SequenceMatcher
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from .models import Profile

class pay(TemplateView):
    template_name='paypro.html'

def conf(request,user):
    return render(request,'confirmation.html',{'user':user})

"""class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"""

class userlist(ListView):
    model=models.Profile
    template_name='userlist.html'
    context_object_name='userlist'

def remu(request,user):
    user=User.objects.get(username=user)
    profile=Profile.objects.get(user=user)
    profile.delete()
    user.is_active = False
    user.save()
    return redirect("accounts:userlist")



class confirms(TemplateView):
    template_name='confirms.html'

class suc(TemplateView):
    template_name='suc.html'


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Tarrif account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return  redirect('accounts:confirms')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

"""def signup(request):
    if request.method == 'POST':
        username=request.POST['Username']
        password=request.POST['Password']
        password1=request.POST['Password1']
        email=request.POST['Email']
        max_similarity = 0.7
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            messages.info(request,"Username already exist")
            print("*********************************")
            print("user already")
        elif(password != password1):
            raise ValidationError("Password and Confirm password does not match")
        elif SequenceMatcher(a=password.lower(), b=username.lower()).quick_ratio() > max_similarity:
            raise serializers.ValidationError("The password is too similar to the username.")
        elif SequenceMatcher(a=password.lower(), b=email.lower()).quick_ratio() > max_similarity:
            raise serializers.ValidationError("The password is too similar to the email.")
        else:
            u=User()
            u.username=username
            u.set_password(password)
            u.email=email
            u.is_active = False
            u.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': u,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(u.pk)),
                'token':account_activation_token.make_token(u),
            })
            email = EmailMessage(
                        mail_subject, message, to=[email]
            )
            email.send()
            return  redirect('accounts:confirms')
        return redirect('accounts:login')"""


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect("test")
    else:
        return HttpResponse('Activation link is invalid!')

User= get_user_model()

@login_required
def member(request,username):
    info = get_object_or_404(models.Profile, user=request.user)
    if request.method=='POST':
        form=forms.ProfileForm(request.POST or None,instance=info)
        if form.is_valid():
            instance=form.save(commit=False)
            if 'image' in request.FILES:
                instance.image=request.FILES['image']
            instance.status=True
            instance.save()
            messages.warning(request, "Your Personal Details Has Been Updated")
            return redirect('accounts:profile',username=username)

    else:
        form=forms.ProfileForm(instance=info)
    return render(request,'profile1.html',{'form':form})




"""@method_decorator(login_required, name='dispatch')
class profile(View):

    def get(self, request, username):
        if request.user.username == username:
            info = get_object_or_404(models.Profile, user=request.user)
            return render(request, 'profile.html', {'info': info})
        else:
            raise Http404"""

@login_required
def profile(request,username):
    info = get_object_or_404(models.Profile, user=request.user)
    return render(request, 'profile.html', {'info': info})
