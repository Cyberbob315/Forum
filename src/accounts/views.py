from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import (
    JsonResponse,
    HttpResponseRedirect,
    HttpResponse
)
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from . import forms


@login_required(login_url='accounts:login')
def user_profile(request, student_id):
    return render(request, 'accounts/user-profile.html',
                  {'student_id': student_id, 'is_edit': False})


@login_required(login_url='accounts:login')
def user_profile_edit(request, student_id):
    return render(request, 'accounts/user-profile.html',
                  {'student_id': student_id, 'is_edit': True})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method != 'POST':
        return render(request, 'accounts/login.html', {'is_error': False})
    student_id = request.POST.get('student_id')
    password = request.POST.get('password')

    user = authenticate(username=student_id, password=password)
    if user is None:
        return render(request, 'accounts/login.html', {'is_error': True})
    login(request, user)
    return HttpResponseRedirect(reverse('home'))


@require_http_methods(['POST'])
def update_profile(request, student_id):
    user = request.user
    if not user.is_superuser or user.student_id != student_id:
        return HttpResponse('You dont have permission to do this')
    validate_form = forms.StudentUpdateForm(request.POST)
    if not validate_form.is_valid():
        return JsonResponse({'success': False, 'email': False}, status=400)
    user.private_email = request.POST['email']
    user.mobile_phone = request.POST['phone']
    user.home_address = request.POST['address']
    if 'profile_pic' in request.FILES:
        user.profile_pic = request.FILES.get('profile_pic')
    user.save()
    return JsonResponse({'success': True, 'email': True}, status=200)


@require_http_methods(['POST'])
def update_image(request, student_id):
    user = request.user
    if 'profile_pic' in request.FILES:
        user.profile_pic = request.FILES.get('profile_pic')
    user.save()
    return JsonResponse({'success': True})
