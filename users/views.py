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
        # if username is not None and password is not None and password2 is not None and email is not None and CompareFlag :
        if len(errors) == 0:
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
    from users import models
    # 获得当前的数据
    Query_User = auth.models.User.objects.filter(id=id)
    Query_UserProFile = models.UserProfile.objects.filter(user_id=id)
    tmpUsr = list(Query_User)[0]
    tmpUsrProfile = list(Query_UserProFile)[0]
    if Query_User.exists() == False:
        return render(request,'error.html',{'message':'can not find user'})
    if tmpUsr.username != str(request.user):
        return render(request,'error.html',{'message':'have not authority'})

    return render(request,'profile.html',{'User':tmpUsr,'UserProfile':tmpUsrProfile})

def change(request,id):
    from users import models
    if request.method == 'POST':
        # 修改信息
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        User = auth.models.User.objects.get(id=id)
        UserProFile = models.UserProfile.objects.get(user_id=id)
        User.email = email
        User.save()

        UserProFile.nickname = nickname
        UserProFile.age = age
        UserProFile.gender = gender
        UserProFile.save()

        return redirect('/users/%d/'%(id,))
    # 获得当前的数据
    Query_User = auth.models.User.objects.filter(id=id)
    Query_UserProFile = models.UserProfile.objects.filter(user_id=id)
    tmpUsr = list(Query_User)[0]
    tmpUsrProfile = list(Query_UserProFile)[0]
    if Query_User.exists() == False:
        return render(request,'error.html',{'message':'can not find user'})
    if tmpUsr.username != str(request.user):
        return render(request,'error.html',{'message':'have not authority'})

    return render(request,'change.html',{'User':tmpUsr,'UserProfile':tmpUsrProfile})