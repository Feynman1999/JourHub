from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth

# 登陆
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(request,username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponse('Username = %s <br>Password = %s' % (username,password))
    else:
        return HttpResponse('Name or PassWord Error')
        

# 注册
def register(request):
    errors = []
    username = None
    password = None
    password2 = None
    email = None
    CompareFlag = False

    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('用户名不能为空')
        else:
            username = request.POST.get('username')

        if not request.POST.get('password'):
            errors.append('密码不能为空')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('确认密码不能为空')
        else:
            password2 = request.POST.get('password2')
        if not request.POST.get('email'):
            errors.append('邮箱不能为空')
        else:
            email = request.POST.get('email')

        if password is not None:
            if password == password2:
                CompareFlag = True
            else:
                errors.append('两次输入密码不一致')
        # 验证成功
        if username is not None and password is not None and password2 is not None and email is not None and CompareFlag :
            user = auth.User.objects.create_user(username,email,password)
            user.save()

            userlogin = auth.authenticate(username = username,password = password)
            auth.login(request,userlogin)
            # 需要填
            return redirect('')
    return render(request,'users/register.html', {'errors': errors})

# 退出
def logout(request):
    auth.logout(request)
    # 需要填
    return redirect('')

# 查看用户信息
def profile(request,id):
    return HttpResponse('UserProfile id is %d<br>Username is %s' %(id,request.user))