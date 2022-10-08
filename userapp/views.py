from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from userapp.forms import CustomPasswordChangeForm, CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'signup.html', {'signup_form':form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'signup_form':form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'login.html', {'login_form':form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'login_form':form})

def logout(request):
    auth.logout(request)
    return redirect('main')

#마이페이지
def mypage(request):
    image = request.user.user_image
    return render(request, 'mypage.html', {'image':image})

#프로필 이미지 수정
def mypage_edit(request):
    if request.method == 'POST':
        info_change_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if info_change_form.is_valid():
            info_change_form.save()
            image = request.user.user_image
            return render(request, 'mypage.html', {'image':image})
    else:
        info_change_form = CustomUserChangeForm(instance=request.user)
        image = request.user.user_image
        return render(request, 'mypage_edit.html', {
            'info_change_form':info_change_form,
            'image':image})

# 비밀번호 수정
def password_edit(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            image = request.user.user_image
            return render(request, 'mypage.html', {'image':image})
    else:
        password_change_form = CustomPasswordChangeForm(request.user)
        image = request.user.user_image
        return render(request, 'password_edit.html', {
            'password_change_form':password_change_form,
            'image':image})