from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('Users/',views.userlist.as_view(),name='userlist'),
    path('processing/',views.pay.as_view(),name='pay'),
    path('Remove-user/<slug:user>',views.remu,name='remu'),
    path('confirmation/<slug:user>',views.conf,name='conf'),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    #path('signup/', views.SignUp.as_view(), name="signup"),
    path('signup/',views.signup,name='signup'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('profile/<slug:username>/update/',views.member,name='profile_update'),
    path('profile/<slug:username>/',views.profile,name='profile'),
    path('confirm/',views.confirms.as_view(),name='confirms'),
    path('success/',views.suc.as_view(),name='suc'),

]
