from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import auth
from users import models
# 登陆
def login(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    if request.method == 'POST':
        errors = []
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "":
            errors.append('请填写用户名')
        if password == "":
            errors.append('请填写密码')
        if len(errors) == 0:
            try:
                tmpuser = auth.models.User.objects.get(username=username)
            except models.User.DoesNotExist:
                errors.append('用户名不存在')
        if len(errors) == 0:
            user = auth.authenticate(request,username=username,password=password)
            if user is None:
                errors.append('密码错误')
        if len(errors) == 0:
            auth.login(request,user)
            return redirect(referer)
        else:
            #提示哪里错了
            return render(request, 'users/login.html',{'message':errors,'PageFlag':True})
    else:
        return render(request, 'users/login.html',{'PageFlag':True})

# 注册
def register(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
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
            if len(list(auth.models.User.objects.filter(username = username))) != 0:
                errors.append('用户名已被使用')

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
            # print(gender)
        if request.POST.get('age'):
            age = request.POST.get('age')
        
        # 验证成功
        if len(errors) == 0:
            user = auth.models.User.objects.create_user(username,email,password)
            user.save()
            userlogin = auth.authenticate(username = username,password = password)
            auth.login(request,userlogin)
            number = auth.models.User.objects.get(username=username)
            print(number.id)
            models.UserProfile.objects.create(user_id=number.id,gender=gender,age=age)
            # 跳转首页
            return redirect('/')
        else:
            return render(request,'users/register.html', {'errors': errors,'PageFlag':True})
    return render(request,'users/register.html',{'PageFlag':True})

# 退出
def logout(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    auth.logout(request)
    return redirect(referer)

# 查看用户信息
def profile(request):
    # 获得当前的数据
    if request.user.is_authenticated == False:
        return redirect('/')
    if request.user.is_staff:
        now_id = request.GET.get('id')
    if now_id == None:
        now_id = request.user.id
    try:
        Query_User = auth.models.User.objects.get(id=now_id)
    except models.User.DoesNotExist:
        return render(request,'error.html',{'message':'can not find user'})
    try:
        Query_UserProFile = models.UserProfile.objects.get(user_id=now_id)
    except models.UserProfile.DoesNotExist:
        return render(request,'users/profile.html',{'User':Query_User})
    return render(request,'users/profile.html',{'User':Query_User,'UserProfile':Query_UserProFile})

# 修改个人信息
def change(request):
    now_id = request.user.id
    if request.method == 'POST':
        # 修改信息
        errors = []
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        if nickname == "":
            errors.append("请填写昵称")
        if email == "":
            errors.append("请填写邮箱")
        if age == "":
            errors.append("请填写年龄")
        if gender == "":
            errors.append("请填写性别")
        if len(errors) != 0:
            return render(request,'users/change.html',{'User':auth.models.User.objects.get(id=now_id),'message':errors})
        User = auth.models.User.objects.get(id=now_id)
        User.email = email
        User.save()
        try:
            UserProFile = models.UserProfile.objects.get(user_id=now_id)
            UserProFile.nickname = nickname
            UserProFile.age = age
            UserProFile.gender = gender
            UserProFile.save()
        except models.UserProfile.DoesNotExist:
            UserProFile = models.UserProfile.objects.create(user_id=now_id,nickname=nickname,age=age,gender=gender)
        # referer = request.META.get('HTTP_REFERER', reverse('profile'))
        return redirect('/users/profile/')
    # 获得当前的数据
    try:
        Query_User = auth.models.User.objects.get(id=now_id)
    except models.User.DoesNotExist:
        return render(request,'error.html',{'message':'can not find user'})
    try:
        Query_UserProFile = models.UserProfile.objects.get(user_id=now_id)
    except models.UserProfile.DoesNotExist:
        return render(request,'users/change.html',{'User':Query_User})
    return render(request,'users/change.html',{'User':Query_User,'UserProfile':Query_UserProFile})
    

# 修改密码
def password(request):
    from django.contrib.auth.hashers import check_password,make_password
    if request.method == 'POST':
        errors = []
        oldpw = request.POST.get('oldpw')
        newpw = request.POST.get('newpw')
        newpw2 = request.POST.get('newpw2')
        if oldpw == "":
            errors.append('请填写旧密码')
        if newpw == "":
            errors.append('请填写新密码')
        if newpw2 == "":
            errors.append('请确认密码')
        referer = request.META.get('HTTP_REFERER', reverse('index'))
        tmpUser = auth.models.User.objects.get(id=request.user.id)
        if len(errors) == 0:
            if check_password(oldpw, tmpUser.password):
                if newpw != newpw2:
                    print(newpw,newpw2)
                    errors.append('两次密码输入不一致')
                else:
                    tmpUser.password = make_password(newpw)
                    tmpUser.save()
                    print('change pw succ')
                    userlogin = auth.authenticate(username = request.user.username,password = newpw)
                    auth.login(request,userlogin)
            else:
                errors.append('旧密码不正确')
        if len(errors) == 0:
            return redirect('/')
        else:
            return render(request,'users/password.html',{'message':errors,'PageFlag':True})
    return render(request,'users/password.html')