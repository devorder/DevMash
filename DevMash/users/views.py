from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Message, Profile, Skill
from .forms import CustomUserCreationForm, EditProfileForm, AddSkillForm, SendMessageForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .utills import search, paginate_projects

# Create your views here.
def user_profile(request):
    profiles,search_query = search(request)
    custom_range,profiles,paginator = paginate_projects(request, profiles, 3)
    return render(request, 'users/profiles.html', context={'profiles': profiles, 'search_query':search_query,'paginator': paginator, 'custom_range': custom_range})

def profile(request, user_id):
    user = Profile.objects.get(id=user_id)
    top_skills = user.skill_set.exclude(description__exact="")
    other_skills = user.skill_set.filter(description="")
    return render(request, 'users/profile.html', context={'user': user, 'top_skills':top_skills, 'other_skills':other_skills})

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('user-profile')

    if(request.method == 'POST'):
        username = request.POST['username'].lower()
        password = request.POST['password']

        # validate data
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username does not exists')
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'edit-account')
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, 'users/login_register.html', context={'page': page})

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User created Successfully")
            page = 'login'
        else:
            messages.error(request, "Sorry some error occured, please try again")

    return render(request, 'users/login_register.html', { 'page': page, 'form': form})

def logoutUser(request):
    logout(request)
    messages.success(request, "User logged out successfully.")
    return redirect('login')

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    top_skills = profile.skill_set.all()
    projects = profile.project_set.all()
    ctx = {'profile': profile, 'top_skills': top_skills, 'projects':projects}
    return render(request, 'users/account.html', ctx)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = EditProfileForm(instance=profile)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-account')
        else:
            messages.success(request, "Something went wrong.")
    ctx = {
        'form': form,
        'action': 'user-account'
    }
    return render(request, 'users/form.html', ctx)

@login_required(login_url='login')
def add_skill(request):
    form = AddSkillForm()
    if request.method == 'POST':
        form = AddSkillForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill added successfully.")
            return redirect('user-account')

    ctx = {'form': form, 'action': 'add-skill'}
    return render(request, 'users/form.html', ctx)

@login_required(login_url='login')
def delete_skill(request, skill_id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=skill_id)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully.")
        return redirect('user-account')
    return render(request, 'delete_template.html', context={'data' : skill})

@login_required(login_url='login')
def edit_skill(request, skill_id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=skill_id)
    form = AddSkillForm(instance=skill)
    if request.method == 'POST':
        form = AddSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully.")
            return redirect('user-account')

    ctx = {'form': form, 'action': 'edit-skill', 'data': skill}
    return render(request, 'users/form.html', ctx)

@login_required(login_url='login')
def inbox(request):
    ctx = {}
    try:
        profile = request.user.profile
        msgs = profile.messages.all()
        unread = msgs.filter(is_read = False).count()
        ctx['msgs'] = msgs
        ctx['unread'] = unread
    except ObjectDoesNotExist:
        ctx['msgs'] = None
        messages.success(request, 'No Messages found')

    return render(request, 'users/inbox.html', ctx)

def inbox_message(request, message_id):
    try:
        msg = Message.objects.get(id= message_id)
        update_msg = msg
        update_msg.is_read = True
        update_msg.save()
        ctx = {
            'msg': msg
        }
        return render(request, 'users/message.html', ctx)
    except (ObjectDoesNotExist, ValidationError) as e:
        return redirect(('inbox'))

def send_message(request, receiver_id):
    form = SendMessageForm(initial={'recipient': receiver_id})
    sender = request.user

    if sender.is_authenticated:
        form = SendMessageForm(initial={'name': sender.profile.name, 'email': sender.profile.email, 'recipient': receiver_id})
        
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        msg = form.save(commit=False)
        msg.sender = None
        if request.user.is_authenticated:
            msg.sender = request.user.profile
        msg.save()
        messages.success(request, 'Message sent successfully.')
        return redirect('profile', user_id=receiver_id)
    
    ctx = {
        'form' : form
    }
    return render(request, 'users/message_form.html', ctx)