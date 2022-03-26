import datetime
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect

# DJANGO
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# CURRENT APPS
from .models import Account, AccountForm, Category,Post, PostForm,Tag,Message, WorkHistory, WorkHistoryForm
from .passwordvalidator import password_check

# -------------------------------------------ACCOUNT----------------------------------------------------------------
# register
def register_view(request):
    if request.user.is_anonymous:
        first_name = ''
        last_name = ''
        username = ''
        email = ''
        contact = ''
        id_name = ''
        id_link = ''
        address = ''
        error=''
        account_type=''
        if request.method == 'POST':
            first_name = request.POST['first_name'].strip().capitalize()
            last_name = request.POST['last_name'].strip().capitalize()
            email = request.POST['email'].lower()
            username = request.POST['username'].strip().lower()
            contact = request.POST['contact']
            address = request.POST['address']
            try:
                account_type = request.POST['account_type']
                if account_type == 'Creator':
                    account_type=True
                elif account_type=='Business Advertisor':
                    account_type=False
            except:
                account_type=''
            id_name = request.POST['id_name']
            id_link = request.POST['id_link']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if account_type =='':
                error="Select one of the option from Account Type dropdown."
            elif first_name == '':
                error = "First name is required."
            elif last_name == '':
                error = "Last name is required."
            elif email == '':
                error = "Email address is required."
            elif username == '':
                error = "Username is required."
            elif address =='':
                error = "Address is required."
            elif id_name =='':
                error = "Youtube / Business Name is required."
            elif id_link == '':
                error ="Youtube link / Business Url is required."
            else:
                try:
                    user = User.objects.get(username=username)
                    error = 'Username already exists'
                except:
                    try:
                        user = User.objects.get(email=email)
                        error = 'Email address already exists.'
                    except:
                        result = password_check(password1, password2)
                        if result == '':
                            error = ''
                            user = User.objects.create_user(
                                first_name=first_name,
                                last_name=last_name,
                                username=username,email=email,
                                password=password1
                                )
                            print(account_type)
                            Account.objects.create(
                                user=user,
                                creator=account_type,
                                contact=contact,
                                address=address,
                                id_name=id_name,
                                id_link=id_link
                                )
                            login(request, user)
                            return redirect('home')
                        else:
                            error = result
        print(account_type)
        return render(request, 'accounts/register.html', {
            'error': error,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'id_name':id_name,
            'id_link':id_link,
            'address':address,
            "contact":contact,
            "account_type":account_type
            })
    else:
        return redirect('home')

# login
def login_view(request):
    username = ''
    password = ''
    error = ''
    next =''
    if request.GET.get('next') is None:
        next='home'
    else:
        next =request.GET.get('next')
    if request.user.is_anonymous:
        if request.method == 'POST':
            username = request.POST['username'].strip().lower()
            password = request.POST['password']
            # login by username
            try:
                username = User.objects.get(username=username)
                user = authenticate(
                    request, username=username.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(next)
                else:
                    error = 'Username / Password is incorrect.'
            except:
                pass
            # login by email
            try:
                username = User.objects.get(email=username)
                user = authenticate(
                    request,
                    username=username.username,
                    password=password
                    )
                if user is not None:
                    login(request, user)
                    return redirect(next)
                else:
                    error = 'Username / Password is incorrect.'
            except:
                pass
        context = {
            "error": error,
            "username": username
            }
        return render(request, 'accounts/login.html', context)
    else:
        return redirect(next)

# logout
def logout_view(request):
    logout(request)
    return redirect('login')

# forgot password
def forgotpassword_view(request):
    context = {}
    return render(request, 'accounts/forgotpassword.html', context)

# -------------------------------------------CREATOR PANEL | Homepage ----------------------------------------------------------------
# creator panel list
@login_required
def creatorpanel_listview(request):
    Creators=[]
    Real_Creators=[]
    if request.method =='POST':
        name = request.POST['name'].split()
        for i in name:
            firstname=User.objects.all().filter(first_name__contains=i)
            for i in firstname:
                if not i in Creators:
                    Creators.append(i)
            lastname=User.objects.all().filter(last_name__contains=i)
            for i in lastname:
                if not i in Creators:
                    Creators.append(i)
    for i in Creators:
        try:
            Real_Creators.append(Account.objects.get(user=i, creator=True))
        except:
            pass
    context={
        "Post":Post.objects.all(),
        "Tag":Tag.objects.all(),
        "Creators":Real_Creators,
        "Categories":Category.objects.all()
    }
    return render(request, 'creator/creatorpanel_list.html', context)

# category filter
@login_required
def categoryfilter_listview(request, category):
    Creators=[]
    Posts=[]
    if request.method =='POST':
        name = request.POST['name'].split()
        for i in name:
            firstname=User.objects.all().filter(first_name__contains=i)
            for i in firstname:
                if not i in Creators:
                    Creators.append(i)
            lastname=User.objects.all().filter(last_name__contains=i)
            for i in lastname:
                if not i in Creators:
                    Creators.append(i)
    try:
        Posts = Post.objects.all().filter(category=Category.objects.get(title=category))
    except:
        Posts =[]
    context={
        "Post":Posts,
        "Tag":Tag.objects.all(),
        "Creators":Creators,
        "Categories":Category.objects.all(),
    }
    return render(request, 'creator/creatorpanel_list.html', context)

# tag filter
@login_required
def tagfilter_listview(request, tag):
    Creators=[]
    Posts=[]
    if request.method =='POST':
        name = request.POST['name'].split()
        for i in name:
            firstname=User.objects.all().filter(first_name__contains=i)
            # for i in firstname:
            #     if not i in Creators:
            #         Creators.append(Account.objects.get(user=i, account))
            lastname=User.objects.all().filter(last_name__contains=i)
            for i in lastname:
                if not i in Creators:
                    Creators.append(i)
    try:
        Posts = Post.objects.all().filter(tags=Tag.objects.get(title=tag))
    except:
        Posts =[]
    context={
        "Post":Posts,
        "Tag":Tag.objects.all(),
        "Creators":Creators,
        "Categories":Category.objects.all(),
    }
    return render(request, 'creator/creatorpanel_list.html', context)

# -------------------------------------------BUSINESS PANEL----------------------------------------------------------------
# business panel list
@login_required
def businesspanel_listview(request):
    Business=[]
    Real_Business=[]
    if request.method =='POST':
        name = request.POST['name'].split()
        for i in name:
            firstname=User.objects.all().filter(first_name__contains=i)
            for i in firstname:
                if not i in Business:
                    Business.append(i)
            lastname=User.objects.all().filter(last_name__contains=i)
            for i in lastname:
                if not i in Business:
                    Business.append(i)
    for i in Business:
        try:
            Real_Business.append(Account.objects.get(user=i, creator=False))
        except:
            pass
    context={
        "Account":Account.objects.filter(creator=False),
        "Business":Real_Business,
        "Categories":Category.objects.all()
    }
    return render(request, 'business/businesspanel_list.html', context)

# -------------------------------------------USER DETAIL----------------------------------------------------------------
# user detail
@login_required
def profile_view(request, name):
    user_account =Account.objects.get(user=request.user)
    verified = user_account.verified
    num_post = len(Post.objects.filter(creator=user_account))
    can_post =0
    available_post=0
    if verified:
        can_post =5-num_post
        available_post=5-num_post
    else:
        can_post=3-num_post
        available_post=3-num_post
    if can_post>0:
        can_post=True
    else:
        can_post=False
    if request.method == 'POST' and can_post:
        form = PostForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.creator = Account.objects.get(user=request.user)
            profile = profile.save()
    else:
        form = PostForm()
    context={
        "Account":Account.objects.get(user__username=name),
        "form":form,
        "num_post":num_post,
        "can_post":can_post,
        "verified":verified,
        "available_post":available_post,
        "WorkHistory":WorkHistory.objects.filter(account=Account.objects.get(user=request.user)),
        "Categories":Category.objects.all(),
        "Post":Post.objects.all().filter(creator=Account.objects.get(user=User.objects.get(username=name))),
    }
    return render(request, 'profile.html', context)

def updateprofile_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name'].strip().capitalize()
        last_name = request.POST['last_name'].strip().capitalize()
        email = request.POST['email'].lower()
        instance = get_object_or_404(Account, id=Account.objects.get(user=request.user).id)
        form = AccountForm(request.POST or None, request.FILES, instance=instance)
        if form.is_valid():
            User.objects.filter(username=request.user).update(
                first_name=first_name,
                last_name=last_name,
                email=email
                )
            form.save()
            return redirect('profile', name=request.user)
        form = AccountForm(request.POST)
    else:
        form = AccountForm()
    context={
        "form":form,
        "Categories":Category.objects.all(),
    }
    return render(request, 'updateprofile.html', context)

# -------------------------------------------MESSAGE----------------------------------------------------------------
# message detail
@login_required
def message_detailview(request, name):
    Messages=[]
    if request.method =='POST':
        message = request.POST['message']
        Message.objects.create(reciever=User.objects.get(username=name), sender=User.objects.get(username=request.user), content=message)
    context={
        "Categories":Category.objects.all(),
        "Messages":(Message.objects.all().filter(
            reciever=User.objects.get(username=name),
        sender=User.objects.get(username=request.user)) | Message.objects.all().filter(
            reciever=User.objects.get(username=request.user),
        sender=User.objects.get(username=name))).order_by('id')
        }
    return render(request, 'messages/messages_detail.html', context)

# message detail
@login_required
def message_listview(request, name):
    Account=[]
    for i in Message.objects.filter(reciever=request.user):
        if not i.sender in Account:
            Account.append(i.sender)
    context={"Account":Account}
    return render(request, 'messages/messages_list.html', context)
# -------------------------------------------DAY COUNTER----------------------------------------------------------------
@login_required
def daycounter_view(request):
    result=''
    if request.method == 'POST':
        initdate = request.POST['initdate']
        finaldate = request.POST['finaldate']
        finaldate=datetime.date(int(finaldate[0:4]),int(finaldate[5:7]),int(finaldate[8:10]))
        initdate=datetime.date(int(initdate[0:4]),int(initdate[5:7]),int(initdate[8:10]))
        result=(finaldate-initdate).days
        
    context={
        "Categories":Category.objects.all(),
        "Result":result,
        }
    return render(request, 'others/daycounter.html', context)

# -------------------------------------------ABOUTVIEW----------------------------------------------------------------
@login_required
def about_view(request):
    context={
        "Categories":Category.objects.all(),
    }
    return render(request, 'others/about.html', context)

# -------------------------------------------MEDIA VIEW----------------------------------------------------------------
@login_required
def media_detailview(request, id):
    context={
        "Categories":Category.objects.all(),
        "Post":Post.objects.get(id=id),
        }
    return render(request, 'media/media_detail.html', context)

# -------------------------------------------Create Post----------------------------------------------------------------

def deletepost(request, id):
    Post.objects.get(id=id).delete()
    return redirect('profile', name=request.user)


def deleteworkhistory(request, id):
    WorkHistory.objects.get(id=id).delete()
    return redirect('profile', name=request.user)

def createworkhistory(request):
    if request.method == 'POST':
        form = WorkHistoryForm(request.POST)
        if form.is_valid():
            workhistory = form.save(commit=False)
            workhistory.account = Account.objects.get(user=request.user)
            workhistory = workhistory.save()
            return redirect('profile', name=request.user)
    else:
        form = WorkHistoryForm()
    context={
        "form":form,
    }
    return render(request, 'createworkhistory.html', context)