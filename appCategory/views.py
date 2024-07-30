from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission,User,ContentType
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail

from .models import CustomUser, Role ,Category ,Feature
from appSection.models import Section

from .forms import (CustomUserCreationForm,
                     CustomUserChangeForm, RoleForm 
                     ,CategoryForm,inlineformset_factory)

from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)
import json
from django.views.decorators.csrf import csrf_exempt


@login_required
@user_passes_test(lambda u: u.is_superuser)
def list_users(request):
    users = CustomUser.objects.all()
    roles = Role.objects.all()
    features = Feature.objects.all()  
    actions = ['view', 'add', 'delete', 'change']
    permissions = []

    for feature in features:
        feature_permissions = {'feature': feature.name, 'actions': []}
        for action in actions:
            perm_name = f'{action}_{feature.name}'
            try:
                content_type = ContentType.objects.get_for_model(feature)
                perm, created = Permission.objects.get_or_create(codename=perm_name, content_type=content_type)
                feature_permissions['actions'].append({'action': action, 'perm_id': perm.id})
            except ContentType.DoesNotExist:
                continue
        permissions.append(feature_permissions)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        selected_permissions = request.POST.getlist('permissions')
        selected_roles = request.POST.getlist('roles')
        user = get_object_or_404(CustomUser, id=user_id)

        # Clear existing permissions and roles
        user.user_permissions.clear()
        user.roles.clear()

        # Add selected permissions
        for perm_id in selected_permissions:
            perm = get_object_or_404(Permission, id=perm_id)
            user.user_permissions.add(perm)

        # Add selected roles and their associated permissions
        for role_id in selected_roles:
            role = get_object_or_404(Role, id=role_id)
            user.roles.add(role)
            for perm in role.permissions.all():
                user.user_permissions.add(perm)

        messages.success(request, f"Roles and permissions have been successfully updated for {user.username}.")
        return redirect('list_users')

    return render(request, 'list_users.html', {
        'users': users,
        'roles': roles,
        'permissions': permissions,
        'features': features,
        'actions': actions
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_user_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_permissions = user.user_permissions.values_list('id', flat=True)
    return JsonResponse({'permissions': list(user_permissions)})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@permission_required('Compliance_app.view_category', raise_exception=True)
def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 3) # Show the number of categories accordingly

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'category_list.html', {
        'page_obj': page_obj,
        'categories': page_obj.object_list,
    })



def category_create(request, pk=None):
    category = None
    if pk:
        category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=category)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.save()

            # Handle the many-to-many relationship
            existing_section_ids = request.POST.getlist('sections')
            category.sections.set(existing_section_ids)

            return redirect('category_list')
    else:
        category_form = CategoryForm(instance=category)

    sections = Section.objects.all()
    print(sections)  

    return render(request, 'category_form.html', {
        'category_form': category_form,
        'sections': sections,
        'category': category,
    })


@login_required
@permission_required('Compliance_app.change_category', raise_exception=True)
def category_update(request, pk):
    section=Section.objects.all()
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            new_section_name = request.POST.get('new_section_name')
            new_section_description = request.POST.get('new_section_description')

            if new_section_name:
                Section.objects.create(
                    name=new_section_name,
                    description=new_section_description,
                    category=category
                )
            return redirect('category_list')
    else:
        category_form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {
        'category_form': category_form,
        'section':section,
    })


@login_required
@permission_required('Compliance_app.delete_category', raise_exception=True)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # section=Section.objects.all()
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})



def section_list(request):
    sections = Section.objects.all()
    return render(request,'section_list.html', {'sections': sections})



def category_section_view(request):
    categories = Category.objects.all()
    selected_category = None
    selected_sections = []
    selected_section = None

    if 'category_id' in request.POST:
        selected_category_id = request.POST.get('category_id')
        if selected_category_id:
            selected_category = Category.objects.get(id=selected_category_id)
            selected_sections = selected_category.sections.all()

    if 'section_id' in request.POST:
        selected_section_id = request.POST.get('section_id')
        if selected_section_id:
            selected_section = Section.objects.get(id=selected_section_id)          

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'selected_sections': selected_sections,
        'selected_section': selected_section,
    }

    return render(request, 'category_section.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_user_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_permissions = user.user_permissions.values_list('id', flat=True)
    return JsonResponse({'permissions': list(user_permissions)})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_users')  
        else:

            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_form.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'user_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('list_user')
    return render(request, 'user_confirm_delete.html', {'user': user})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def role_list(request):
    roles = Role.objects.all()
    permissions = Permission.objects.all()

    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        role = get_object_or_404(Role, id=role_id)
        selected_permissions = request.POST.getlist('permissions')
        role.permissions.set(Permission.objects.filter(codename__in=selected_permissions))
        role.save()
        return redirect('role_list')

    role_permissions = {
        role.id: {
            'view': role.permissions.filter(codename='view').exists(),
            'add': role.permissions.filter(codename='add').exists(),
            'edit': role.permissions.filter(codename='edit').exists(),
            'delete': role.permissions.filter(codename='delete').exists()
        } for role in roles
    }

    return render(request, 'role_list.html', {
        'roles': roles,
        'role_permissions': role_permissions
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'role_form.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'role_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('role_list')
    return render(request, 'role_confirm_delete.html', {'role': role})

def send_registration_email(user_email):
    subject = 'Welcome !!! To Carols App'
    message = 'Thank you for registering. Enjoy the Service ;) '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_registration_email(user.email)  # Send the registration email
            messages.success(request, f'{user.username} have successfully registered on Carol\'s app')  # Success message
            return redirect('dashboard')
        else:
            messages.error(request, 'Form is not valid. Please correct the errors.')  # Error message
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                if user.is_superuser:
                    return redirect('dashboard')  
                else:
                    return redirect('dashboard') 
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# @login_required
def dashboard(request):
    return render(request, 'dashboard.html')



@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')



import openai

client = OpenAI()
@csrf_exempt
def chat_with_gpt(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        response = openai.Completion.create(
            model="gpt-3.5-turbo",  
            prompt=user_message,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        gpt_message = response.choices[0].text.strip()
        return JsonResponse({'message': gpt_message})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def workout_view(request):
    return render(request, 'workout.html')