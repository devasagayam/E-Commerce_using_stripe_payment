from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Profile
# Create your views here.
@csrf_exempt
def home(request):
    info=Profile.objects.get(user=request.user)

    return render(request,'test.html',{'info':info})

def test(request):
    return render(request,'tests.html')

def invice(request):
    return render(request,'invice.html')
