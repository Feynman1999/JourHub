from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from users import models
# 登陆
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/..')
        else:
            return redirect('/..')
    else:
        redirect('/..')

# 注册
def register(request):
    errors = []
    username = None
    password = None
    password2 = None
    email = None
    gender = None
    age = None
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
        if request.POST.get('gender'):
            gender = request.POST.get('gender')
        if request.POST.get('age'):
            age = request.POST.get('age')
        # 验证成功
        if len(errors) == 0:
        # if username is not None and password is not None and password2 is not None and email is not None and CompareFlag :
            user = auth.models.User.objects.create_user(username,email,password)
            user.save()
            userlogin = auth.authenticate(username = username,password = password)
            auth.login(request,userlogin)
            number = auth.models.User.objects.filter(username=username).values('id')
            print(number[0]['id'])
            from users import models
            models.UserProfile.objects.create(user_id=number[0]['id'],gender=gender,age=age)
            # 跳转首页
            return redirect('/..')
        else:
            return render(request,'register.html', {'Errors': errors})
    return render(request,'register.html')

# 退出
def logout(request):
    auth.logout(request)
    # 需要填
    return redirect('/..')

# 查看用户信息
def profile(request,id):
    Query_User = auth.models.User.objects.filter(id=id)
    
    if Query_User.exists() == False:
        return render(request,'error.html',{'Message':'can not find user'})
    if Query_User.username == request.user:
        return render(request,'profile.html',{})
    else:
        return render(request,'error.html',{'Message':'have not authority'})
    